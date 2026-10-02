from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import ModelBase
from app.models.enums import TipoEmpresa

if TYPE_CHECKING:
    from app.models.logistica import Carga, Motorista, Veiculo, Viagem
    from app.models.usuario import EmpresaUsuario


class Empresa(ModelBase, Base):
    __tablename__ = "empresas"

    nome: Mapped[str] = mapped_column(String(180), nullable=False, index=True)
    documento: Mapped[str | None] = mapped_column(String(40), unique=True)
    tipo: Mapped[TipoEmpresa] = mapped_column(
        Enum(TipoEmpresa, name="tipo_empresa"),
        nullable=False,
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    usuarios: Mapped[list[EmpresaUsuario]] = relationship(back_populates="empresa")
    veiculos: Mapped[list[Veiculo]] = relationship(back_populates="empresa")
    motoristas: Mapped[list[Motorista]] = relationship(back_populates="empresa")
    viagens_transportadora: Mapped[list[Viagem]] = relationship(
        back_populates="transportadora",
        foreign_keys="Viagem.transportadora_id",
    )
    cargas_produtor: Mapped[list[Carga]] = relationship(
        back_populates="produtor",
        foreign_keys="Carga.produtor_id",
    )
    cargas_cliente: Mapped[list[Carga]] = relationship(
        back_populates="cliente",
        foreign_keys="Carga.cliente_id",
    )
