from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.iot import Medicao
    from app.models.logistica import Caixa, Carga, Viagem


class DadoExterno(ModelBase, Base):
    __tablename__ = "dados_externos"

    viagem_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("viagens.id"))
    carga_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("cargas.id"))
    caixa_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("caixas.id"))
    fonte: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(String(120), nullable=False)
    dados: Mapped[dict] = mapped_column(JSONB, nullable=False)
    coletado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    viagem: Mapped[Viagem | None] = relationship(back_populates="dados_externos")
    carga: Mapped[Carga | None] = relationship(back_populates="dados_externos")
    caixa: Mapped[Caixa | None] = relationship(back_populates="dados_externos")


class LeituraExterna(ModelBase, Base):
    __tablename__ = "leituras_externas"
    __table_args__ = (
        UniqueConstraint(
            "origem",
            "channel_id",
            "entry_id",
            "field_name",
            name="uq_leitura_externa_origem_channel_entry_field",
        ),
        Index("ix_leituras_externas_medicao_id", "medicao_id"),
        Index("ix_leituras_externas_origem_channel", "origem", "channel_id"),
    )

    origem: Mapped[str] = mapped_column(String(80), nullable=False)
    channel_id: Mapped[str] = mapped_column(String(80), nullable=False)
    entry_id: Mapped[int] = mapped_column(nullable=False)
    field_name: Mapped[str] = mapped_column(String(40), nullable=False)
    medicao_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("medicoes.id"),
        nullable=False,
    )

    medicao: Mapped[Medicao] = relationship(back_populates="leitura_externa")
