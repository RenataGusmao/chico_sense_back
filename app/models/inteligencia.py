from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.logistica import Caixa, Carga, Viagem


class RecomendacaoIA(ModelBase, Base):
    __tablename__ = "recomendacoes_ia"

    viagem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("viagens.id"),
        nullable=False,
    )
    carga_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("cargas.id"))
    caixa_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("caixas.id"))
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    nivel_risco: Mapped[str | None] = mapped_column(String(80))
    justificativa: Mapped[str | None] = mapped_column(Text)
    fatores_considerados: Mapped[dict | None] = mapped_column(JSONB)
    gerada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    viagem: Mapped[Viagem] = relationship(back_populates="recomendacoes_ia")
    carga: Mapped[Carga | None] = relationship(back_populates="recomendacoes_ia")
    caixa: Mapped[Caixa | None] = relationship(back_populates="recomendacoes_ia")
