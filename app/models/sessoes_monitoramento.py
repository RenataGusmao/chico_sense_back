"""Carga-specific declarations and temporal monitoring sessions (no sensor ingestion)."""
import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean, CheckConstraint, DateTime, ForeignKey, ForeignKeyConstraint,
    Index, Integer, JSON, Numeric, String, Text, UniqueConstraint, text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import ModelBase


class MaturacaoCarga(str, PyEnum):
    VERDE_MADURA = "VERDE_MADURA"
    EM_AMADURECIMENTO = "EM_AMADURECIMENTO"
    MADURA = "MADURA"
    MISTA = "MISTA"
    DESCONHECIDA = "DESCONHECIDA"


class StatusSessao(str, PyEnum):
    ATIVA = "ATIVA"
    ENCERRADA = "ENCERRADA"
    CANCELADA = "CANCELADA"


MATURACAO_CHECK = "maturacao IN ('VERDE_MADURA','EM_AMADURECIMENTO','MADURA','MISTA','DESCONHECIDA')"


class CargaMonitoramento(ModelBase, Base):
    __tablename__ = "cargas_monitoramento"
    __table_args__ = (
        UniqueConstraint("carga_id", name="uq_config_monitoramento_carga"),
        UniqueConstraint("id", "carga_id", name="uq_config_monitoramento_id_carga"),
        CheckConstraint("massa_kg > 0 AND massa_kg < 100000000", name="ck_config_monitoramento_massa"),
        CheckConstraint(MATURACAO_CHECK, name="ck_config_monitoramento_maturacao"),
        CheckConstraint("produto_identificado = 'MANGA_TOMMY_ATKINS'", name="ck_config_monitoramento_produto"),
        CheckConstraint("versao > 0", name="ck_config_monitoramento_versao"),
    )
    carga_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cargas.id"), nullable=False)
    produto_identificado: Mapped[str] = mapped_column(String(40), nullable=False)
    massa_kg: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    maturacao: Mapped[str] = mapped_column(String(30), nullable=False)
    lote_codigo: Mapped[str] = mapped_column(String(120), nullable=False)
    lote_hipotetico: Mapped[bool] = mapped_column(Boolean, nullable=False)
    rastreabilidade: Mapped[str] = mapped_column(Text, nullable=False)
    versao: Mapped[int] = mapped_column(Integer, nullable=False)
    atualizado_por_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)


class SessaoMonitoramento(ModelBase, Base):
    __tablename__ = "sessoes_monitoramento"
    __table_args__ = (
        ForeignKeyConstraint(["carga_id", "viagem_id"], ["cargas.id", "cargas.viagem_id"], name="fk_sessao_carga_viagem"),
        ForeignKeyConstraint(["configuracao_id", "carga_id"], ["cargas_monitoramento.id", "cargas_monitoramento.carga_id"], name="fk_sessao_config_carga"),
        UniqueConstraint("criada_por_id", "chave_idempotencia", name="uq_sessao_autor_idempotencia"),
        CheckConstraint("estado IN ('ATIVA','ENCERRADA','CANCELADA')", name="ck_sessao_estado"),
        CheckConstraint("(estado = 'ATIVA' AND fim IS NULL AND finalizada_por_id IS NULL AND motivo_fim IS NULL) OR (estado <> 'ATIVA' AND fim IS NOT NULL AND fim > inicio AND finalizada_por_id IS NOT NULL AND motivo_fim IS NOT NULL)", name="ck_sessao_ciclo"),
        CheckConstraint("sensor_umidade_id IS NULL OR sensor_umidade_id <> sensor_temperatura_id", name="ck_sessao_sensores_distintos"),
        CheckConstraint("massa_kg > 0 AND massa_kg < 100000000", name="ck_sessao_massa"),
        CheckConstraint(MATURACAO_CHECK, name="ck_sessao_maturacao"),
        CheckConstraint("ambiente_aquisicao IN ('LABORATORIO','TRANSPORTE_REFRIGERADO')", name="ck_sessao_ambiente"),
        Index("ix_sessoes_viagem_inicio", "viagem_id", "inicio"),
        Index("ix_sessoes_carga_inicio", "carga_id", "inicio"),
        Index("uq_sessao_ativa_carga", "carga_id", unique=True, postgresql_where=text("estado = 'ATIVA'"), sqlite_where=text("estado = 'ATIVA'")),
        Index("uq_sessao_ativa_temperatura", "sensor_temperatura_id", unique=True, postgresql_where=text("estado = 'ATIVA'"), sqlite_where=text("estado = 'ATIVA'")),
        Index("uq_sessao_ativa_umidade", "sensor_umidade_id", unique=True, postgresql_where=text("estado = 'ATIVA'"), sqlite_where=text("estado = 'ATIVA'")),
    )
    carga_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    viagem_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("viagens.id"), nullable=False)
    configuracao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fim: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    sensor_temperatura_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sensores.id"), nullable=False)
    sensor_umidade_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("sensores.id"))
    ambiente_aquisicao: Mapped[str] = mapped_column(String(30), nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text)
    # Snapshot: later edits to the cargo declaration never rewrite past sessions.
    configuracao_versao: Mapped[int] = mapped_column(Integer, nullable=False)
    produto_identificado: Mapped[str] = mapped_column(String(40), nullable=False)
    massa_kg: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    maturacao: Mapped[str] = mapped_column(String(30), nullable=False)
    lote_codigo: Mapped[str] = mapped_column(String(120), nullable=False)
    lote_hipotetico: Mapped[bool] = mapped_column(Boolean, nullable=False)
    rastreabilidade: Mapped[str] = mapped_column(Text, nullable=False)
    origem_sensor: Mapped[dict] = mapped_column(JSON().with_variant(JSONB(), "postgresql"), nullable=False)
    criada_por_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    finalizada_por_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    motivo_fim: Mapped[str | None] = mapped_column(Text)
    chave_idempotencia: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    assinatura_requisicao: Mapped[str] = mapped_column(String(64), nullable=False)


class EventoMonitoramento(ModelBase, Base):
    __tablename__ = "eventos_monitoramento"
    configuracao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cargas_monitoramento.id"), nullable=False, index=True)
    sessao_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("sessoes_monitoramento.id"), index=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False)
    registrado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dados: Mapped[dict] = mapped_column(JSON().with_variant(JSONB(), "postgresql"), nullable=False)
