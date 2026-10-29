"""Immutable public contracts; no ORM, web framework or environment settings."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum

from .parametros import DATA_CONSULTA, FONTE, REFERENCIA, TAXAS, VERSAO_MODELO, PontoReferencia

Numero = Decimal | int | float | str | None


class ModoCalculo(str, Enum):
    MODO_RESTRITO = "MODO_RESTRITO"
    MODO_EXPLORATORIO = "MODO_EXPLORATORIO"


class EstagioMaturacao(str, Enum):
    VERDE_MADURA = "VERDE_MADURA"
    EM_AMADURECIMENTO = "EM_AMADURECIMENTO"
    MADURA = "MADURA"
    MISTA = "MISTA"
    DESCONHECIDA = "DESCONHECIDA"


class StatusCalculo(str, Enum):
    ENTRADA_INVALIDA = "ENTRADA_INVALIDA"
    CONFIGURACAO_INCOMPLETA = "CONFIGURACAO_INCOMPLETA"
    SEM_ESTIMATIVA = "SEM_ESTIMATIVA"
    PARCIAL = "PARCIAL"
    COMPLETO_NO_MODELO = "COMPLETO_NO_MODELO"


class Motivo(str, Enum):
    MASSA_INVALIDA = "MASSA_INVALIDA"
    UNIDADE_MASSA_INVALIDA = "UNIDADE_MASSA_INVALIDA"
    JANELA_INVALIDA = "JANELA_INVALIDA"
    HORARIO_INVALIDO = "HORARIO_INVALIDO"
    HORARIO_FUTURO = "HORARIO_FUTURO"
    IDENTIDADE_INVALIDA = "IDENTIDADE_INVALIDA"
    IDENTIDADE_CONTRADITORIA = "IDENTIDADE_CONTRADITORIA"
    MATURACAO_INVALIDA = "MATURACAO_INVALIDA"
    MODO_INVALIDO = "MODO_INVALIDO"
    MODO_AUSENTE = "MODO_AUSENTE"
    INTERVALO_MAXIMO_INVALIDO = "INTERVALO_MAXIMO_INVALIDO"
    INTERVALO_MAXIMO_AUSENTE = "INTERVALO_MAXIMO_AUSENTE"
    CONFLITO_OBSERVACAO = "CONFLITO_OBSERVACAO"
    TEMPERATURA_INVALIDA = "TEMPERATURA_INVALIDA"
    UNIDADE_TEMPERATURA_INVALIDA = "UNIDADE_TEMPERATURA_INVALIDA"
    FORA_DO_DOMINIO = "FORA_DO_DOMINIO"
    SEM_TAXA_NO_MODO = "SEM_TAXA_NO_MODO"
    LACUNA_EXCESSIVA = "LACUNA_EXCESSIVA"
    BORDA_SEM_LEITURA = "BORDA_SEM_LEITURA"
    SEM_LEITURAS = "SEM_LEITURAS"
    RESOLUCAO_APRESENTACAO = "RESOLUCAO_APRESENTACAO"
    LIMITE_ARITMETICO = "LIMITE_ARITMETICO"


@dataclass(frozen=True)
class LeituraTemperatura:
    medida_em: datetime
    temperatura: Numero
    sensor_id: str
    sessao_id: str
    unidade: str = "C"
    identificador_externo: str | None = None
    recebida_em: datetime | None = None


@dataclass(frozen=True)
class EntradaEstimativa:
    massa: Numero
    inicio: datetime
    fim: datetime
    sensor_id: str
    sessao_id: str
    leituras: tuple[LeituraTemperatura, ...] = ()
    intervalo_maximo_s: Numero = None
    modo: ModoCalculo | str | None = ModoCalculo.MODO_RESTRITO
    maturacao: EstagioMaturacao | str | None = EstagioMaturacao.DESCONHECIDA
    unidade_massa: str = "kg"
    corte_aquisicao: datetime | None = None

    def __post_init__(self) -> None:
        # Copy mutable collections provided by callers, without changing their data.
        object.__setattr__(self, "leituras", tuple(self.leituras))


@dataclass(frozen=True)
class ObservacaoNormalizada:
    medida_em: datetime
    temperatura_c: Decimal | None
    originais: tuple[LeituraTemperatura, ...]
    motivos: tuple[Motivo, ...] = ()


@dataclass(frozen=True)
class IntervaloEstimativa:
    inicio: datetime
    fim: datetime
    duracao_s: Decimal
    temperatura_inicio_c: Decimal | None = None
    taxa_min_ul_kg_h: Decimal | None = None
    taxa_max_ul_kg_h: Decimal | None = None
    volume_min_ul: Decimal | None = None
    volume_max_ul: Decimal | None = None
    motivos: tuple[Motivo, ...] = ()

    @property
    def coberto(self) -> bool:
        return not self.motivos


@dataclass(frozen=True)
class ResultadoEstimativa:
    status_calculo: StatusCalculo
    massa_kg: Decimal | None
    inicio: datetime | None
    fim: datetime | None
    modo: ModoCalculo | None
    maturacao: EstagioMaturacao | None
    intervalo_maximo_s: Decimal | None
    corte_aquisicao: datetime | None
    sensor_id: str
    sessao_id: str
    entrada: EntradaEstimativa | None = None
    tabela_referencia: tuple[PontoReferencia, ...] = TAXAS
    cobertura: Decimal | None = None
    volume_coberto_min_ul: Decimal | None = None
    volume_coberto_max_ul: Decimal | None = None
    volume_janela_min_ul: Decimal | None = None
    volume_janela_max_ul: Decimal | None = None
    duracao_janela_s: Decimal | None = None
    duracao_coberta_s: Decimal | None = None
    duracao_nao_coberta_s: Decimal | None = None
    percentual_cobertura: Decimal | None = None
    observacoes: tuple[ObservacaoNormalizada, ...] = ()
    intervalos: tuple[IntervaloEstimativa, ...] = ()
    duplicatas_descartadas: int = 0
    motivos: tuple[Motivo, ...] = ()
    limitacoes: tuple[str, ...] = ()
    interpolacao_utilizada: bool = False
    perfil: str | None = None
    metodologia: str = "Retencao a esquerda, dois extremos validos, sem extensao de bordas."
    unidade_volume: str = "µL"
    versao_modelo: str = VERSAO_MODELO
    fonte: str = FONTE
    referencia: str = REFERENCIA
    data_consulta: str = DATA_CONSULTA
    aplicabilidade: str = "REFERENCIA_GERAL_NAO_VALIDADA_PARA_TOMMY_ATKINS"
    classificacao_risco_etileno: str = "NAO_AVALIADO"
    motivo_risco: str = "SEM_LIMIAR_VALIDADO"
