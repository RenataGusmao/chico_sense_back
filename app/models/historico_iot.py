"""Immutable source bindings, acquisition attempts and session reading provenance."""
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, ForeignKeyConstraint, Index, Integer, JSON, Numeric, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import ModelBase


class FonteSessaoIoT(ModelBase, Base):
    __tablename__ = "fontes_sessao_iot"
    __table_args__ = (
        UniqueConstraint("sessao_id", "sensor_id", name="uq_fonte_sessao_sensor"),
        UniqueConstraint("sessao_id", "channel_id", "field_name", name="uq_fonte_sessao_channel_field"),
        UniqueConstraint("id", "sessao_id", name="uq_fonte_id_sessao"),
    )
    sessao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessoes_monitoramento.id"), nullable=False)
    sensor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sensores.id"), nullable=False)
    origem: Mapped[str] = mapped_column(String(20), nullable=False)
    channel_id: Mapped[str] = mapped_column(String(80), nullable=False)
    field_name: Mapped[str] = mapped_column(String(40), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    contexto: Mapped[str] = mapped_column(String(30), nullable=False)
    unidade: Mapped[str] = mapped_column(String(30), nullable=False)
    snapshot: Mapped[dict] = mapped_column(JSON().with_variant(JSONB(), "postgresql"), nullable=False)


class SincronizacaoIoT(ModelBase, Base):
    __tablename__ = "sincronizacoes_iot"
    __table_args__ = (
        UniqueConstraint("sessao_id", "chave_idempotencia", name="uq_sync_sessao_chave"),
        UniqueConstraint("sessao_id", "revisao", name="uq_sync_sessao_revisao"),
        UniqueConstraint("id", "sessao_id", name="uq_sync_id_sessao"),
        CheckConstraint("revisao > 0 AND fim_janela >= inicio_janela", name="ck_sync_janela_revisao"),
        CheckConstraint("estado IN ('EM_EXECUCAO','CONCLUIDA','PARCIAL','FALHA','INTERROMPIDA')", name="ck_sync_estado"),
        Index("uq_sync_executando_sessao", "sessao_id", unique=True, postgresql_where=text("estado = 'EM_EXECUCAO'"), sqlite_where=text("estado = 'EM_EXECUCAO'")),
    )
    sessao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessoes_monitoramento.id"), nullable=False)
    usuario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    revisao: Mapped[int] = mapped_column(Integer, nullable=False)
    chave_idempotencia: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    assinatura: Mapped[str] = mapped_column(String(64), nullable=False)
    origem_dados: Mapped[str] = mapped_column(String(20), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    inicio_janela: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fim_janela: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    iniciada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finalizada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expira_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    complementacao: Mapped[bool] = mapped_column(Boolean, nullable=False)
    justificativa: Mapped[str | None] = mapped_column(Text)
    resumo: Mapped[dict] = mapped_column(JSON().with_variant(JSONB(), "postgresql"), nullable=False)


class RegistroSessaoIoT(ModelBase, Base):
    __tablename__ = "registros_sessao_iot"
    __table_args__ = (
        ForeignKeyConstraint(["fonte_id", "sessao_id"], ["fontes_sessao_iot.id", "fontes_sessao_iot.sessao_id"], name="fk_registro_fonte_sessao"),
        ForeignKeyConstraint(["sincronizacao_id", "sessao_id"], ["sincronizacoes_iot.id", "sincronizacoes_iot.sessao_id"], name="fk_registro_sync_sessao"),
        UniqueConstraint("fonte_id", "entry_id", name="uq_registro_fonte_entry"),
        CheckConstraint("entry_id > 0", name="ck_registro_entry"),
        CheckConstraint("(estado = 'VALIDA' AND valor IS NOT NULL AND medicao_id IS NOT NULL) OR (estado = 'INVALIDA' AND valor IS NULL AND medicao_id IS NULL)", name="ck_registro_estado"),
        Index("ix_registro_sessao_medida", "sessao_id", "medida_em", "id"),
    )
    sessao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessoes_monitoramento.id"), nullable=False)
    fonte_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    sincronizacao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    medicao_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("medicoes.id"))
    entry_id: Mapped[int] = mapped_column(Integer, nullable=False)
    medida_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    timestamp_origem: Mapped[str] = mapped_column(String(80), nullable=False)
    recebida_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    processada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    valor: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    motivo: Mapped[str | None] = mapped_column(String(80))
    assinatura: Mapped[str] = mapped_column(String(64), nullable=False)
    tardia: Mapped[bool | None] = mapped_column(Boolean)
    apos_encerramento: Mapped[bool] = mapped_column(Boolean, nullable=False)
    fora_de_ordem: Mapped[bool] = mapped_column(Boolean, nullable=False)


class OcorrenciaIoT(ModelBase, Base):
    __tablename__ = "ocorrencias_iot"
    sincronizacao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sincronizacoes_iot.id"), nullable=False, index=True)
    fonte_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("fontes_sessao_iot.id"))
    entry_id: Mapped[int | None] = mapped_column(Integer)
    medida_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    codigo: Mapped[str] = mapped_column(String(80), nullable=False)
    detalhes: Mapped[dict] = mapped_column(JSON().with_variant(JSONB(), "postgresql"), nullable=False)

    processada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
