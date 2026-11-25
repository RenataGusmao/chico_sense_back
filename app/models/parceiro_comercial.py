"""Explicit carrier/partner approval; never an account membership or read grant."""
import uuid
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, String, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import ModelBase


class ParceiroComercial(ModelBase, Base):
    __tablename__ = 'parceiros_comerciais'
    __table_args__ = (
        UniqueConstraint('transportadora_id', 'empresa_id', name='uq_parceiro_transportadora_empresa'),
        CheckConstraint('transportadora_id <> empresa_id', name='ck_parceiro_empresas_distintas'),
        Index('ix_parceiro_transportadora_ativo', 'transportadora_id', 'ativo'),
    )
    transportadora_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('empresas.id'), nullable=False)
    empresa_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('empresas.id'), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    aprovado_por_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False)
    atualizado_por_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False)
    justificativa: Mapped[str] = mapped_column(String(2000), nullable=False)
