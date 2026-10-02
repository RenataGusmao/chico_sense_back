from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import ModelBase
from app.models.enums import ContextoMedicao, StatusDispositivo, StatusSensor, TipoSensor

if TYPE_CHECKING:
    from app.models.integracoes import LeituraExterna
    from app.models.logistica import Caixa, Carga, Veiculo, Viagem
    from app.models.monitoramento import Alerta


class Dispositivo(ModelBase, Base):
    __tablename__ = "dispositivos"

    identificador: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[StatusDispositivo] = mapped_column(
        Enum(StatusDispositivo, name="status_dispositivo"),
        default=StatusDispositivo.ATIVO,
        nullable=False,
    )
    veiculo_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("veiculos.id"),
    )
    viagem_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("viagens.id"),
    )
    carga_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cargas.id"),
    )

    veiculo: Mapped[Veiculo | None] = relationship(back_populates="dispositivos")
    viagem: Mapped[Viagem | None] = relationship(back_populates="dispositivos")
    carga: Mapped[Carga | None] = relationship(back_populates="dispositivos")
    sensores: Mapped[list[Sensor]] = relationship(back_populates="dispositivo")


class Sensor(ModelBase, Base):
    __tablename__ = "sensores"
    __table_args__ = (
        UniqueConstraint("dispositivo_id", "identificador", name="uq_sensor_dispositivo_identificador"),
    )

    dispositivo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("dispositivos.id"),
        nullable=False,
    )
    identificador: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[TipoSensor] = mapped_column(Enum(TipoSensor, name="tipo_sensor"), nullable=False)
    contexto: Mapped[ContextoMedicao] = mapped_column(
        Enum(ContextoMedicao, name="contexto_medicao"),
        nullable=False,
    )
    unidade: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[StatusSensor] = mapped_column(
        Enum(StatusSensor, name="status_sensor"),
        default=StatusSensor.ATIVO,
        nullable=False,
    )

    dispositivo: Mapped[Dispositivo] = relationship(back_populates="sensores")
    medicoes: Mapped[list[Medicao]] = relationship(back_populates="sensor")


class Medicao(ModelBase, Base):
    __tablename__ = "medicoes"
    __table_args__ = (
        Index("ix_medicoes_medida_em", "medida_em"),
        Index("ix_medicoes_sensor_id", "sensor_id"),
        Index("ix_medicoes_viagem_id", "viagem_id"),
        Index("ix_medicoes_carga_id", "carga_id"),
        Index("ix_medicoes_caixa_id", "caixa_id"),
        Index("ix_medicoes_sensor_medida_em", "sensor_id", "medida_em"),
    )

    sensor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sensores.id"),
        nullable=False,
    )
    viagem_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("viagens.id"),
    )
    carga_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cargas.id"),
    )
    caixa_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("caixas.id"),
    )
    medida_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    contexto: Mapped[ContextoMedicao] = mapped_column(
        Enum(ContextoMedicao, name="contexto_medicao"),
        nullable=False,
    )
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    unidade: Mapped[str] = mapped_column(String(30), nullable=False)

    sensor: Mapped[Sensor] = relationship(back_populates="medicoes")
    viagem: Mapped[Viagem | None] = relationship(back_populates="medicoes")
    carga: Mapped[Carga | None] = relationship(back_populates="medicoes")
    caixa: Mapped[Caixa | None] = relationship(back_populates="medicoes")
    alertas: Mapped[list[Alerta]] = relationship(back_populates="medicao")
    leitura_externa: Mapped[LeituraExterna | None] = relationship(back_populates="medicao")
