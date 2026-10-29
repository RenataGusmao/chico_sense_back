"""Queries only. Transaction ownership belongs to the monitoring use case."""
from uuid import UUID
from datetime import datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from app.models.sessoes_monitoramento import CargaMonitoramento, SessaoMonitoramento


class MonitoramentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def configuracao(self, carga_id: UUID) -> CargaMonitoramento | None:
        return self.db.scalar(select(CargaMonitoramento).where(CargaMonitoramento.carga_id == carga_id))

    def repeticao(self, autor_id: UUID, chave: UUID) -> SessaoMonitoramento | None:
        return self.db.scalar(select(SessaoMonitoramento).where(
            SessaoMonitoramento.criada_por_id == autor_id,
            SessaoMonitoramento.chave_idempotencia == chave,
        ))

    def conflito(self, carga_id: UUID, sensores: list[UUID], inicio: datetime) -> bool:
        # New ATIVA session reserves [inicio, infinity). Terminal sessions keep
        # their historical reservations, including cancelled demonstration data.
        query = select(SessaoMonitoramento.id).where(
            or_(SessaoMonitoramento.carga_id == carga_id,
                SessaoMonitoramento.sensor_temperatura_id.in_(sensores),
                SessaoMonitoramento.sensor_umidade_id.in_(sensores)),
            or_(SessaoMonitoramento.fim.is_(None), SessaoMonitoramento.fim > inicio),
        ).limit(1)
        return self.db.scalar(query) is not None

    def ativa(self, carga_id: UUID) -> bool:
        return self.db.scalar(select(SessaoMonitoramento.id).where(
            SessaoMonitoramento.carga_id == carga_id, SessaoMonitoramento.estado == "ATIVA",
        ).limit(1)) is not None

    def listar(self, *, carga_id: UUID | None = None, viagem_id: UUID | None = None,
               limit: int = 50, offset: int = 0) -> list[SessaoMonitoramento]:
        query = select(SessaoMonitoramento)
        if carga_id is not None:
            query = query.where(SessaoMonitoramento.carga_id == carga_id)
        if viagem_id is not None:
            query = query.where(SessaoMonitoramento.viagem_id == viagem_id)
        return list(self.db.scalars(query.order_by(
            SessaoMonitoramento.inicio, SessaoMonitoramento.id,
        ).limit(limit).offset(offset)))
