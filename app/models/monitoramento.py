from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import ModelBase
from app.models.enums import NivelAlerta, StatusAlerta

if TYPE_CHECKING:
    from app.models.iot import Medicao
    from app.models.logistica import Caixa, Carga, Viagem


class Alerta(ModelBase, Base):
    __tablename__ = "alertas"

    viagem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("viagens.id"),
        nullable=False,
    )
    carga_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("cargas.id"))
    caixa_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("caixas.id"))
    medicao_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("medicoes.id"),
    )
    tipo: Mapped[str] = mapped_column(String(120), nullable=False)
    nivel: Mapped[NivelAlerta] = mapped_column(
        Enum(NivelAlerta, name="nivel_alerta"),
        nullable=False,
    )
    status: Mapped[StatusAlerta] = mapped_column(
        Enum(StatusAlerta, name="status_alerta"),
        default=StatusAlerta.ABERTO,
        nullable=False,
    )
    limite_considerado: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    valor_registrado: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    unidade: Mapped[str | None] = mapped_column(String(30))
    iniciado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finalizado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    duracao_segundos: Mapped[int | None] = mapped_column(Integer)

    viagem: Mapped[Viagem] = relationship(back_populates="alertas")
    carga: Mapped[Carga | None] = relationship(back_populates="alertas")
    caixa: Mapped[Caixa | None] = relationship(back_populates="alertas")
    medicao: Mapped[Medicao | None] = relationship(back_populates="alertas")


class Ocorrencia(ModelBase, Base):
    __tablename__ = "ocorrencias"

    viagem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("viagens.id"),
        nullable=False,
    )
    carga_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("cargas.id"))
    caixa_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("caixas.id"))
    tipo: Mapped[str] = mapped_column(String(120), nullable=False)
    titulo: Mapped[str] = mapped_column(String(180), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    registrada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str | None] = mapped_column(String(80))

    viagem: Mapped[Viagem] = relationship(back_populates="ocorrencias")
    carga: Mapped[Carga | None] = relationship(back_populates="ocorrencias")
    caixa: Mapped[Caixa | None] = relationship(back_populates="ocorrencias")
