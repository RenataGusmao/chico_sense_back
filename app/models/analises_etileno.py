"""Persisted immutable execution; decimal strings in JSON preserve all engine digits."""
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, JSON, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import ModelBase


class AnaliseEtileno(ModelBase, Base):
    __tablename__ = 'analises_etileno'
    __table_args__ = (
        UniqueConstraint('sessao_id', 'chave_idempotencia', name='uq_analise_sessao_chave'),
        CheckConstraint('fim > inicio AND corte_aquisicao >= fim AND executada_em >= corte_aquisicao', name='ck_analise_janela'),
        CheckConstraint('revisao_aquisicao >= 0', name='ck_analise_revisao'),
        CheckConstraint("classificacao_risco_etileno = 'NAO_AVALIADO'", name='ck_analise_risco'),
        CheckConstraint("status_calculo IN ('ENTRADA_INVALIDA','CONFIGURACAO_INCOMPLETA','SEM_ESTIMATIVA','PARCIAL','COMPLETO_NO_MODELO')", name='ck_analise_status'),
        Index('ix_analise_sessao_execucao', 'sessao_id', 'executada_em', 'id'),
    )
    sessao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('sessoes_monitoramento.id'), nullable=False)
    usuario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False)
    chave_idempotencia: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    assinatura_requisicao: Mapped[str] = mapped_column(String(64), nullable=False)
    executada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fim: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    corte_aquisicao: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revisao_aquisicao: Mapped[int] = mapped_column(Integer, nullable=False)
    massa_kg: Mapped[Decimal | None] = mapped_column(Numeric(12,4))
    maturacao: Mapped[str] = mapped_column(String(30), nullable=False)
    modo: Mapped[str] = mapped_column(String(30), nullable=False)
    intervalo_maximo_s: Mapped[Decimal | None] = mapped_column(Numeric(12,3))
    versao_modelo: Mapped[str] = mapped_column(String(80), nullable=False)
    status_calculo: Mapped[str] = mapped_column(String(40), nullable=False)
    classificacao_risco_etileno: Mapped[str] = mapped_column(String(20), nullable=False)
    hash_entrada: Mapped[str] = mapped_column(String(64), nullable=False)
    hash_resultado: Mapped[str] = mapped_column(String(64), nullable=False)
    entrada_snapshot: Mapped[dict] = mapped_column(JSON().with_variant(JSONB(), 'postgresql'), nullable=False)
    resultado: Mapped[dict] = mapped_column(JSON().with_variant(JSONB(), 'postgresql'), nullable=False)
