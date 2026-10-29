"""Transactional monitoring declarations and session lifecycle, without ingestion."""
from contextlib import contextmanager
from datetime import datetime, timezone
from hashlib import sha256
import json
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.enums import StatusCarga, StatusViagem, StatusSensor, StatusDispositivo, TipoSensor, ContextoMedicao
from app.models.iot import Sensor, Dispositivo
from app.models.logistica import Carga, Viagem
from app.models.produto import Produto
from app.models.usuario import Usuario
from app.models.sessoes_monitoramento import CargaMonitoramento, EventoMonitoramento, SessaoMonitoramento
from app.modules.empresas.service import EmpresaService, is_admin
from app.modules.monitoramento.schemas import CargaMonitoramentoPut, SessaoCreate, SessaoFinalizar
from app.repositories.monitoramento import MonitoramentoRepository

CAMPOS_CARGA = ("produto_identificado", "massa_kg", "maturacao", "lote_codigo", "lote_hipotetico", "rastreabilidade")


def utc(value: datetime) -> datetime:
    # SQLite discards timezone metadata; application inputs require AwareDatetime.
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)


class MonitoramentoService:
    def __init__(self, db: Session, user: Usuario):
        self.db, self.user = db, user
        self.repo = MonitoramentoRepository(db)

    @contextmanager
    def transacao(self):
        # Auth may already have autobegun the request's Session; do not nest begin().
        try:
            yield
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(409, "Conflito de integridade ou requisicao simultanea; consulte o estado e tente novamente.") from exc
        except Exception:
            self.db.rollback()
            raise

    def obter(self, model, record_id: UUID, lock: bool = False):
        query = select(model).where(model.id == record_id)
        if lock:
            query = query.with_for_update().execution_options(populate_existing=True)
        record = self.db.scalar(query)
        if record is None:
            raise HTTPException(404, "Registro nao encontrado.")
        return record

    def autorizar_viagem(self, viagem: Viagem, escrita: bool = False) -> None:
        if not self.user.ativo or not self.user.perfil:
            raise HTTPException(403, "Usuario sem permissao para monitoramento.")
        perfil = self.user.perfil.nome
        if perfil not in (("ADMIN", "GESTOR", "OPERADOR") if escrita else ("ADMIN", "GESTOR", "OPERADOR", "CONSULTA")):
            raise HTTPException(403, "Perfil sem permissao para esta operacao.")
        empresa = EmpresaService(self.db).authorize(viagem.transportadora_id, self.user)
        if escrita and not empresa.ativo:
            raise HTTPException(409, "Transportadora inativa.")

    def carga(self, carga_id: UUID, escrita: bool = False) -> tuple[Carga, Viagem]:
        carga = self.obter(Carga, carga_id)
        viagem = self.obter(Viagem, carga.viagem_id, lock=escrita)
        self.autorizar_viagem(viagem, escrita)
        if escrita:
            carga = self.obter(Carga, carga_id, lock=True)
            if carga.viagem_id != viagem.id:
                raise HTTPException(409, "O vinculo da carga foi alterado; repita a operacao.")
        return carga, viagem

    def evento(self, configuracao_id: UUID, tipo: str, dados: dict, sessao_id: UUID | None = None):
        self.db.add(EventoMonitoramento(
            configuracao_id=configuracao_id, sessao_id=sessao_id, usuario_id=self.user.id,
            tipo=tipo, registrado_em=datetime.now(timezone.utc), dados=dados,
        ))

    @staticmethod
    def snapshot(config: CargaMonitoramento) -> dict:
        return {campo: str(getattr(config, campo)) if campo == "massa_kg" else getattr(config, campo)
                for campo in CAMPOS_CARGA}

    def configurar(self, carga_id: UUID, data: CargaMonitoramentoPut) -> CargaMonitoramento:
        with self.transacao():
            carga, viagem = self.carga(carga_id, escrita=True)
            config = self.repo.configuracao(carga_id)
            valores = data.model_dump()
            if config is not None and all(getattr(config, k) == v for k, v in valores.items()):
                return config  # Exact PUT replay is a no-op, including audit/version.
            if carga.status in (StatusCarga.ENTREGUE, StatusCarga.CANCELADA) or viagem.status in (StatusViagem.CONCLUIDA, StatusViagem.CANCELADA):
                raise HTTPException(409, "Carga ou viagem encerrada nao permite alterar a declaracao.")
            if not self.obter(Produto, carga.produto_id).ativo:
                raise HTTPException(409, "Produto cadastrado esta inativo.")
            if self.repo.ativa(carga_id):
                raise HTTPException(409, "Encerre a sessao ativa antes de alterar os dados da carga.")
            antes = self.snapshot(config) if config is not None else None
            if config is None:
                config = CargaMonitoramento(carga_id=carga_id, versao=1, atualizado_por_id=self.user.id, **valores)
                self.db.add(config)
            else:
                for chave, valor in valores.items():
                    setattr(config, chave, valor)
                config.versao += 1
                config.atualizado_por_id = self.user.id
            self.db.flush()
            self.evento(config.id, "CARGA_CONFIGURADA", {"antes": antes, "depois": self.snapshot(config), "versao": config.versao})
        return config

    def consultar_configuracao(self, carga_id: UUID) -> CargaMonitoramento:
        self.carga(carga_id)
        config = self.repo.configuracao(carga_id)
        if config is None:
            raise HTTPException(404, "Carga ainda nao configurada para monitoramento.")
        return config

    def sensores(self, data: SessaoCreate, carga: Carga, viagem: Viagem) -> dict:
        ids = [data.sensor_temperatura_id] + ([data.sensor_umidade_id] if data.sensor_umidade_id else [])
        if len(set(ids)) != len(ids):
            raise HTTPException(422, "Sensores de temperatura e umidade devem ser distintos.")
        registros = {}
        # Lock stable parent rows even when there is no previous session to lock.
        for sensor_id in sorted(ids, key=str):
            registros[sensor_id] = self.obter(Sensor, sensor_id, lock=True)
        origem = {}
        for papel, sensor_id, tipo in (
            ("temperatura", data.sensor_temperatura_id, TipoSensor.TEMPERATURA),
            ("umidade", data.sensor_umidade_id, TipoSensor.UMIDADE),
        ):
            if sensor_id is None:
                origem[papel] = None
                continue
            sensor = registros[sensor_id]
            dispositivo = self.obter(Dispositivo, sensor.dispositivo_id)
            if sensor.tipo != tipo:
                raise HTTPException(422, "Tipo de sensor incompativel com a funcao selecionada.")
            unidades = ("C", "°C", "F", "°F", "K") if tipo == TipoSensor.TEMPERATURA else ("%", "%RH")
            if sensor.unidade not in unidades:
                raise HTTPException(422, "Unidade do sensor nao suportada.")
            if sensor.status != StatusSensor.ATIVO or dispositivo.status != StatusDispositivo.ATIVO:
                raise HTTPException(409, "Sensor ou dispositivo nao esta ativo.")
            vinculos = ((dispositivo.viagem_id, viagem.id), (dispositivo.carga_id, carga.id), (dispositivo.veiculo_id, viagem.veiculo_id))
            if any(atual is not None and atual != esperado for atual, esperado in vinculos):
                raise HTTPException(409, "Dispositivo vinculado a outro contexto logistico.")
            if all(atual is None for atual, _ in vinculos):
                if not is_admin(self.user) or data.ambiente_aquisicao != "LABORATORIO":
                    raise HTTPException(403, "Sensor sem contexto logistico exige ADMIN e ambiente de laboratorio.")
            if data.ambiente_aquisicao == "TRANSPORTE_REFRIGERADO" and sensor.contexto == ContextoMedicao.PROTOTIPO:
                raise HTTPException(422, "Sensor de prototipo nao comprova aquisicao em transporte refrigerado.")
            origem[papel] = {
                "sensor_id": str(sensor.id), "identificador": sensor.identificador,
                "tipo": sensor.tipo.value, "contexto": sensor.contexto.value, "unidade": sensor.unidade,
                "dispositivo_id": str(dispositivo.id), "dispositivo": dispositivo.identificador,
                "vinculos": {"viagem_id": str(dispositivo.viagem_id) if dispositivo.viagem_id else None,
                            "carga_id": str(dispositivo.carga_id) if dispositivo.carga_id else None,
                            "veiculo_id": str(dispositivo.veiculo_id) if dispositivo.veiculo_id else None},
            }
        return origem

    def criar_sessao(self, carga_id: UUID, data: SessaoCreate) -> tuple[SessaoMonitoramento, bool]:
        with self.transacao():
            carga, viagem = self.carga(carga_id, escrita=True)
            assinatura_dados = data.model_dump(mode="json") | {"carga_id": str(carga_id), "inicio": utc(data.inicio).isoformat()}
            assinatura = sha256(json.dumps(assinatura_dados, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            anterior = self.repo.repeticao(self.user.id, data.chave_idempotencia)
            if anterior is not None:
                if anterior.assinatura_requisicao != assinatura:
                    raise HTTPException(409, "Chave idempotente reutilizada com conteudo diferente.")
                return anterior, False
            config = self.repo.configuracao(carga_id)
            if config is None:
                raise HTTPException(409, "Configure os dados de monitoramento da carga primeiro.")
            if viagem.status != StatusViagem.EM_ANDAMENTO or carga.status != StatusCarga.EM_TRANSITO:
                raise HTTPException(409, "Inicio exige viagem em andamento e carga em transito.")
            if not self.obter(Produto, carga.produto_id).ativo:
                raise HTTPException(409, "Produto cadastrado esta inativo.")
            inicio = utc(data.inicio)
            if inicio > datetime.now(timezone.utc):
                raise HTTPException(422, "Inicio efetivo nao pode estar no futuro.")
            if viagem.inicio_real is None or inicio < utc(viagem.inicio_real):
                raise HTTPException(422, "Sessao exige inicio real da viagem anterior ou igual.")
            origem = self.sensores(data, carga, viagem)
            ids = [data.sensor_temperatura_id] + ([data.sensor_umidade_id] if data.sensor_umidade_id else [])
            if self.repo.conflito(carga_id, ids, inicio):
                raise HTTPException(409, "Janela conflitante com outra sessao da carga ou dos sensores.")
            sessao = SessaoMonitoramento(
                carga_id=carga_id, viagem_id=viagem.id, configuracao_id=config.id,
                inicio=inicio, estado="ATIVA", configuracao_versao=config.versao,
                criada_por_id=self.user.id, assinatura_requisicao=assinatura,
                origem_sensor=origem, **{k: getattr(config, k) for k in CAMPOS_CARGA},
                **data.model_dump(exclude={"inicio"}),
            )
            self.db.add(sessao)
            self.db.flush()
            self.evento(config.id, "SESSAO_INICIADA", {"inicio": inicio.isoformat(), "versao_carga": config.versao, "origem_sensor": origem}, sessao.id)
        return sessao, True

    def consultar_sessao(self, sessao_id: UUID) -> SessaoMonitoramento:
        sessao = self.obter(SessaoMonitoramento, sessao_id)
        self.autorizar_viagem(self.obter(Viagem, sessao.viagem_id))
        return sessao

    def listar_carga(self, carga_id: UUID, limit: int, offset: int):
        self.carga(carga_id)
        return self.repo.listar(carga_id=carga_id, limit=limit, offset=offset)

    def listar_viagem(self, viagem_id: UUID, limit: int, offset: int):
        self.autorizar_viagem(self.obter(Viagem, viagem_id))
        return self.repo.listar(viagem_id=viagem_id, limit=limit, offset=offset)

    def finalizar(self, sessao_id: UUID, data: SessaoFinalizar, estado: str) -> SessaoMonitoramento:
        if estado not in ("ENCERRADA", "CANCELADA"):
            raise HTTPException(422, "Estado final invalido.")
        with self.transacao():
            original = self.obter(SessaoMonitoramento, sessao_id)
            _, viagem = self.carga(original.carga_id, escrita=True)
            sessao = self.obter(SessaoMonitoramento, sessao_id, lock=True)
            fim = utc(data.fim)
            if sessao.estado != "ATIVA":
                if sessao.estado == estado and utc(sessao.fim) == fim and sessao.motivo_fim == data.motivo:
                    return sessao
                raise HTTPException(409, "Sessao finalizada e imutavel; nao pode ser reaberta ou alterada.")
            if fim <= utc(sessao.inicio) or fim > datetime.now(timezone.utc):
                raise HTTPException(422, "Fim deve ser posterior ao inicio e nao estar no futuro.")
            if viagem.chegada_em is not None and fim > utc(viagem.chegada_em):
                raise HTTPException(422, "Fim da sessao posterior a chegada real da viagem.")
            if viagem.status == StatusViagem.CANCELADA and estado != "CANCELADA":
                raise HTTPException(409, "Viagem cancelada exige cancelamento da sessao.")
            sessao.estado, sessao.fim = estado, fim
            sessao.finalizada_por_id, sessao.motivo_fim = self.user.id, data.motivo
            self.evento(sessao.configuracao_id, "SESSAO_" + estado, {"fim": fim.isoformat(), "motivo": data.motivo}, sessao.id)
        return sessao
