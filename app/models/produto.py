from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.logistica import Carga


class Produto(ModelBase, Base):
    __tablename__ = "produtos"

    nome: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    parametros: Mapped[list[ParametroProduto]] = relationship(back_populates="produto")
    cargas: Mapped[list[Carga]] = relationship(back_populates="produto")


class ParametroProduto(ModelBase, Base):
    __tablename__ = "parametros_produto"

    produto_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("produtos.id"),
        nullable=False,
    )
    nome_parametro: Mapped[str] = mapped_column(String(120), nullable=False)
    unidade: Mapped[str | None] = mapped_column(String(30))
    valor_minimo: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    valor_maximo: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    observacao: Mapped[str | None] = mapped_column(Text)

    produto: Mapped[Produto] = relationship(back_populates="parametros")
