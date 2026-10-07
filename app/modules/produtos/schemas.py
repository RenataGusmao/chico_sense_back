from decimal import Decimal
from typing import ClassVar
from uuid import UUID

from pydantic import Field

from app.schemas.operacional import Input, Update, Response


class ProdutoCreate(Input):
    nome: str = Field(min_length=1, max_length=120)
    descricao: str | None = None
    ativo: bool = True


class ProdutoUpdate(Update):
    required_fields: ClassVar = ("nome", "ativo")
    nome: str | None = Field(default=None, min_length=1, max_length=120)
    descricao: str | None = None
    ativo: bool | None = None


class ProdutoResponse(Response):
    nome: str
    descricao: str | None
    ativo: bool


class ParametroCreate(Input):
    nome_parametro: str = Field(min_length=1, max_length=120)
    unidade: str | None = Field(default=None, max_length=30)
    valor_minimo: Decimal | None = Field(default=None, max_digits=12, decimal_places=4)
    valor_maximo: Decimal | None = Field(default=None, max_digits=12, decimal_places=4)
    observacao: str | None = None


class ParametroUpdate(Update):
    required_fields: ClassVar = ("nome_parametro",)
    nome_parametro: str | None = Field(default=None, min_length=1, max_length=120)
    unidade: str | None = Field(default=None, max_length=30)
    valor_minimo: Decimal | None = Field(default=None, max_digits=12, decimal_places=4)
    valor_maximo: Decimal | None = Field(default=None, max_digits=12, decimal_places=4)
    observacao: str | None = None


class ParametroResponse(ParametroCreate, Response):
    produto_id: UUID
