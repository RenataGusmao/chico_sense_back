"""Pure interval integration. Callers supply the acquisition cutoff; no clock/I/O."""
from collections import defaultdict
from dataclasses import replace
from datetime import datetime, timezone
from decimal import Context, Decimal, DecimalException, ROUND_HALF_EVEN, localcontext

from .parametros import DATA_CONSULTA, FONTE, LIMITACOES_GERAIS, REFERENCIA, TAXAS, VERSAO_MODELO
from .tipos import (
    EntradaEstimativa, EstagioMaturacao, IntervaloEstimativa, LeituraTemperatura,
    ModoCalculo, Motivo, Numero, ObservacaoNormalizada, ResultadoEstimativa, StatusCalculo,
)

CONTEXTO = Context(prec=50, rounding=ROUND_HALF_EVEN)
ZERO = Decimal(0)


def _decimal(valor: Numero) -> Decimal:
    if isinstance(valor, bool) or not isinstance(valor, (Decimal, int, float, str)):
        raise ValueError("Numero finito obrigatorio.")
    try:
        numero = Decimal(str(valor))
    except DecimalException as exc:
        raise ValueError("Numero invalido.") from exc
    if not numero.is_finite():
        raise ValueError("Numero finito obrigatorio.")
    return numero


def converter_massa(valor: Numero, unidade: str = "kg") -> Decimal:
    """Explicit metric units only; positivity is checked by estimar_etileno."""
    fatores = {"kg": Decimal(1), "g": Decimal("0.001"), "t": Decimal(1000)}
    if unidade not in fatores:
        raise ValueError("Unidade de massa invalida; use kg, g ou t.")
    with localcontext(CONTEXTO):
        return _decimal(valor) * fatores[unidade]


def converter_temperatura(valor: Numero, unidade: str = "C") -> Decimal:
    """No snapping to reference points; C/°C, F/°F and K are explicit."""
    with localcontext(CONTEXTO):
        numero = _decimal(valor)
        if unidade in ("C", "°C"):
            return numero
        if unidade in ("F", "°F"):
            return (numero - 32) * 5 / 9
        if unidade == "K":
            return numero - Decimal("273.15")
    raise ValueError("Unidade de temperatura invalida.")


def _utc(valor: datetime | None) -> datetime | None:
    if not isinstance(valor, datetime) or valor.tzinfo is None or valor.utcoffset() is None:
        return None
    return valor.astimezone(timezone.utc)


def _segundos(inicio: datetime, fim: datetime) -> Decimal:
    delta = fim - inicio
    return Decimal(delta.days * 86400 + delta.seconds) + Decimal(delta.microseconds) / 1000000


def _taxas(temperatura: Decimal, modo: ModoCalculo) -> tuple[Decimal, Decimal] | None:
    if temperatura < TAXAS[0].temperatura_c or temperatura > TAXAS[-1].temperatura_c:
        return None
    for ponto in TAXAS:
        if temperatura == ponto.temperatura_c:
            return ponto.minimo_ul_kg_h, ponto.maximo_ul_kg_h
    if modo == ModoCalculo.MODO_EXPLORATORIO:
        for a, b in zip(TAXAS, TAXAS[1:]):
            if a.temperatura_c < temperatura < b.temperatura_c:
                alfa = (temperatura - a.temperatura_c) / (b.temperatura_c - a.temperatura_c)
                return (
                    a.minimo_ul_kg_h + alfa * (b.minimo_ul_kg_h - a.minimo_ul_kg_h),
                    a.maximo_ul_kg_h + alfa * (b.maximo_ul_kg_h - a.maximo_ul_kg_h),
                )
    return None


def _assinatura(leitura: LeituraTemperatura) -> tuple[str, ...]:
    return (
        leitura.medida_em.astimezone(timezone.utc).isoformat(),
        type(leitura.temperatura).__name__, str(leitura.temperatura), leitura.unidade,
    )


def _normalizar(
    entrada: EntradaEstimativa, inicio: datetime, fim: datetime, corte: datetime,
    modo: ModoCalculo,
) -> tuple[tuple[ObservacaoNormalizada, ...], tuple[Motivo, ...], int]:
    grupos: dict[datetime, list[LeituraTemperatura]] = defaultdict(list)
    identidades: dict[str, list[LeituraTemperatura]] = defaultdict(list)
    selecionadas: list[LeituraTemperatura] = []
    for leitura in entrada.leituras:
        if not isinstance(leitura, LeituraTemperatura):
            return (), (Motivo.IDENTIDADE_INVALIDA,), 0
        if leitura.sensor_id != entrada.sensor_id or leitura.sessao_id != entrada.sessao_id:
            continue
        horario = _utc(leitura.medida_em)
        if horario is None or (leitura.recebida_em is not None and _utc(leitura.recebida_em) is None):
            return (), (Motivo.HORARIO_INVALIDO,), 0
        if not inicio <= horario <= fim:
            continue
        if horario > corte:
            return (), (Motivo.HORARIO_FUTURO,), 0
        if leitura.identificador_externo is not None and (
            not isinstance(leitura.identificador_externo, str) or not leitura.identificador_externo.strip()
        ):
            return (), (Motivo.IDENTIDADE_INVALIDA,), 0
        selecionadas.append(leitura)
        if leitura.identificador_externo is not None:
            identidades[leitura.identificador_externo].append(leitura)
    conflitos: set[datetime] = set()
    for leituras in identidades.values():
        horarios = {_utc(l.medida_em) for l in leituras}
        if len(horarios) > 1:
            return (), (Motivo.IDENTIDADE_CONTRADITORIA,), 0
        if len({_assinatura(l) for l in leituras}) > 1:
            conflitos.update(horarios)
    # Receipt metadata does not change source identity or decide a conflict winner.
    selecionadas.sort(key=lambda l: (
        _assinatura(l), l.identificador_externo or "",
        l.recebida_em.isoformat() if l.recebida_em else "",
    ))
    vistas: set[tuple[str, tuple[str, ...]]] = set()
    duplicatas = 0
    for leitura in selecionadas:
        if leitura.identificador_externo is not None:
            chave = leitura.identificador_externo, _assinatura(leitura)
            if chave in vistas:
                duplicatas += 1
                continue
            vistas.add(chave)
        grupos[_utc(leitura.medida_em)].append(leitura)
    pontos = []
    for horario, leituras in sorted(grupos.items()):
        valores: list[Decimal | None] = []
        motivos: list[Motivo] = []
        for leitura in leituras:
            try:
                valor = converter_temperatura(leitura.temperatura, leitura.unidade)
            except DecimalException:
                return (), (Motivo.LIMITE_ARITMETICO,), duplicatas
            except ValueError:
                valor = None
                motivos.append(
                    Motivo.UNIDADE_TEMPERATURA_INVALIDA
                    if leitura.unidade not in ("C", "°C", "F", "°F", "K")
                    else Motivo.TEMPERATURA_INVALIDA
                )
            valores.append(valor)
        conflito = horario in conflitos or (
            len(valores) > 1 and (None in valores or len(set(valores)) > 1)
        )
        if conflito:
            motivos.insert(0, Motivo.CONFLITO_OBSERVACAO)
            temperatura = None
        else:
            temperatura = valores[0]
            if len(valores) > 1:
                duplicatas += len(valores) - 1
            if temperatura is not None and _taxas(temperatura, modo) is None:
                motivos.append(
                    Motivo.FORA_DO_DOMINIO if temperatura < 10 or temperatura > 20
                    else Motivo.SEM_TAXA_NO_MODO
                )
        pontos.append(ObservacaoNormalizada(
            horario, temperatura, tuple(leituras), tuple(dict.fromkeys(motivos)),
        ))
    return tuple(pontos), (), duplicatas


def _motivos_par(a: ObservacaoNormalizada, b: ObservacaoNormalizada, longo: bool) -> tuple[Motivo, ...]:
    presentes = set(a.motivos + b.motivos)
    if longo:
        presentes.add(Motivo.LACUNA_EXCESSIVA)
    ordem = (
        Motivo.CONFLITO_OBSERVACAO, Motivo.TEMPERATURA_INVALIDA,
        Motivo.UNIDADE_TEMPERATURA_INVALIDA, Motivo.FORA_DO_DOMINIO,
        Motivo.SEM_TAXA_NO_MODO, Motivo.LACUNA_EXCESSIVA,
    )
    return tuple(m for m in ordem if m in presentes)


def _intervalos(
    pontos: tuple[ObservacaoNormalizada, ...], inicio: datetime, fim: datetime,
    massa: Decimal, maximo: Decimal, modo: ModoCalculo,
) -> tuple[IntervaloEstimativa, ...]:
    if not pontos:
        return (IntervaloEstimativa(inicio, fim, _segundos(inicio, fim), motivos=(Motivo.SEM_LEITURAS,)),)
    intervalos: list[IntervaloEstimativa] = []
    if pontos[0].medida_em > inicio:
        intervalos.append(IntervaloEstimativa(
            inicio, pontos[0].medida_em, _segundos(inicio, pontos[0].medida_em),
            motivos=(Motivo.BORDA_SEM_LEITURA,),
        ))
    for a, b in zip(pontos, pontos[1:]):
        duracao = _segundos(a.medida_em, b.medida_em)
        motivos = _motivos_par(a, b, duracao > maximo)
        intervalo = IntervaloEstimativa(a.medida_em, b.medida_em, duracao, a.temperatura_c, motivos=motivos)
        if not motivos:
            minimo, max_taxa = _taxas(a.temperatura_c, modo)
            intervalo = replace(
                intervalo, taxa_min_ul_kg_h=minimo, taxa_max_ul_kg_h=max_taxa,
                volume_min_ul=minimo * massa * duracao / 3600,
                volume_max_ul=max_taxa * massa * duracao / 3600,
            )
        intervalos.append(intervalo)
    if pontos[-1].medida_em < fim:
        intervalos.append(IntervaloEstimativa(
            pontos[-1].medida_em, fim, _segundos(pontos[-1].medida_em, fim),
            motivos=(Motivo.BORDA_SEM_LEITURA,),
        ))
    return tuple(intervalos)


def _arredondar(valor: Decimal) -> Decimal:
    with localcontext(CONTEXTO) as contexto:
        contexto.prec = max(50, valor.adjusted() + 10)
        return valor.quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)


def estimar_etileno(entrada: EntradaEstimativa) -> ResultadoEstimativa:
    """Return explicit unavailability for bad data, never an empty-sum zero.

    No current clock is read: corte_aquisicao defaults to the requested window end.
    Live adapters must explicitly provide their actual acquisition cutoff.
    """
    with localcontext(CONTEXTO):
        return _estimar(entrada)


def _estimar(entrada: EntradaEstimativa) -> ResultadoEstimativa:
    invalidos: list[Motivo] = []
    faltas: list[Motivo] = []
    inicio, fim = _utc(entrada.inicio), _utc(entrada.fim)
    corte = _utc(entrada.corte_aquisicao) if entrada.corte_aquisicao is not None else fim
    if inicio is None or fim is None or fim <= inicio:
        invalidos.append(Motivo.JANELA_INVALIDA)
    if corte is None:
        invalidos.append(Motivo.HORARIO_INVALIDO)
    if not all(isinstance(v, str) and v.strip() for v in (entrada.sensor_id, entrada.sessao_id)):
        invalidos.append(Motivo.IDENTIDADE_INVALIDA)
    massa = None
    if entrada.unidade_massa not in ("kg", "g", "t"):
        invalidos.append(Motivo.UNIDADE_MASSA_INVALIDA)
    else:
        try:
            massa = converter_massa(entrada.massa, entrada.unidade_massa)
            if massa <= 0:
                raise ValueError("Massa deve ser positiva.")
        except (ValueError, DecimalException):
            massa = None
            invalidos.append(Motivo.MASSA_INVALIDA)
    maximo = None
    if entrada.intervalo_maximo_s is None:
        faltas.append(Motivo.INTERVALO_MAXIMO_AUSENTE)
    else:
        try:
            maximo = _decimal(entrada.intervalo_maximo_s)
            if maximo <= 0:
                raise ValueError("Intervalo deve ser positivo.")
        except ValueError:
            maximo = None
            invalidos.append(Motivo.INTERVALO_MAXIMO_INVALIDO)
    modo = None
    if entrada.modo is None:
        faltas.append(Motivo.MODO_AUSENTE)
    else:
        try:
            modo = ModoCalculo(entrada.modo)
        except (ValueError, TypeError):
            invalidos.append(Motivo.MODO_INVALIDO)
    maturacao = None
    try:
        maturacao = EstagioMaturacao(entrada.maturacao) if entrada.maturacao is not None else EstagioMaturacao.DESCONHECIDA
    except (ValueError, TypeError):
        invalidos.append(Motivo.MATURACAO_INVALIDA)
    limitacoes = list(LIMITACOES_GERAIS)
    if maturacao == EstagioMaturacao.DESCONHECIDA:
        limitacoes.append("Maturacao desconhecida: faixa geral nao validada para o estagio da carga.")
    if maturacao == EstagioMaturacao.MISTA:
        limitacoes.append("Maturacao mista: nao se presume uniformidade ou proporcao de estagios.")
    perfil = None
    metodologia = "Retencao a esquerda, dois extremos validos, sem extensao de bordas."
    if modo is not None:
        perfil = "UC_DAVIS_PONTOS_V1"
        if modo == ModoCalculo.MODO_EXPLORATORIO:
            perfil = "UC_DAVIS_LINEAR_EXPLORATORIO_V1"
            metodologia += " Interpolacao linear exploratoria de cada limite entre pontos adjacentes."
            limitacoes.append("Modo exploratorio: interpolacao e hipotese matematica, nao taxa medida na fonte.")
    base = ResultadoEstimativa(
        StatusCalculo.ENTRADA_INVALIDA, massa, inicio, fim, modo, maturacao,
        maximo, corte, entrada.sensor_id, entrada.sessao_id,
        motivos=tuple(dict.fromkeys(invalidos + faltas)), limitacoes=tuple(limitacoes),
        perfil=perfil, metodologia=metodologia, fonte=FONTE, referencia=REFERENCIA,
        data_consulta=DATA_CONSULTA, versao_modelo=VERSAO_MODELO, entrada=entrada,
    )
    if invalidos:
        return base
    # Validate indispensable observation metadata even when G is missing.
    pontos, erros, duplicatas = _normalizar(
        entrada, inicio, fim, corte, modo or ModoCalculo.MODO_RESTRITO,
    )
    if erros:
        return replace(base, motivos=erros + tuple(faltas))
    if faltas:
        return replace(base, status_calculo=StatusCalculo.CONFIGURACAO_INCOMPLETA,
                       observacoes=pontos, duplicatas_descartadas=duplicatas)
    try:
        intervalos = _intervalos(pontos, inicio, fim, massa, maximo, modo)
        duracao = _segundos(inicio, fim)
        cobertos = tuple(i for i in intervalos if i.coberto)
        coberta = sum((i.duracao_s for i in cobertos), ZERO)
        completo = coberta == duracao
        minimo = max_volume = None
        motivos = tuple(sorted({m for i in intervalos for m in i.motivos}, key=lambda m: m.value))
        if cobertos:
            minimo = _arredondar(sum((i.volume_min_ul for i in cobertos), ZERO))
            max_volume = _arredondar(sum((i.volume_max_ul for i in cobertos), ZERO))
            if minimo == 0 or max_volume == 0:
                motivos += (Motivo.RESOLUCAO_APRESENTACAO,)
        status = StatusCalculo.SEM_ESTIMATIVA
        if cobertos:
            status = StatusCalculo.COMPLETO_NO_MODELO if completo else StatusCalculo.PARCIAL
        return replace(
            base, status_calculo=status, observacoes=pontos, intervalos=intervalos,
            duplicatas_descartadas=duplicatas, motivos=motivos,
            volume_coberto_min_ul=minimo, volume_coberto_max_ul=max_volume,
            volume_janela_min_ul=minimo if completo else None,
            volume_janela_max_ul=max_volume if completo else None,
            duracao_janela_s=duracao, duracao_coberta_s=coberta,
            duracao_nao_coberta_s=duracao - coberta, cobertura=coberta / duracao,
            percentual_cobertura=coberta * 100 / duracao,
            interpolacao_utilizada=any(
                i.temperatura_inicio_c not in tuple(p.temperatura_c for p in TAXAS)
                for i in cobertos
            ),
        )
    except DecimalException:
        return replace(base, motivos=(Motivo.LIMITE_ARITMETICO,))
