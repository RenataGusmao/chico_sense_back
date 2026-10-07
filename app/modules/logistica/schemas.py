from datetime import datetime
from decimal import Decimal
from typing import ClassVar
from uuid import UUID

from pydantic import AwareDatetime, Field

from app.models.enums import StatusViagem, StatusCarga, StatusCaixa
from app.schemas.operacional import Input, Update, Response


class VeiculoCreate(Input):
    empresa_id: UUID
    identificador: str = Field(min_length=1, max_length=80)
    placa: str | None = Field(default=None, min_length=1, max_length=20)
    modelo: str | None = Field(default=None, max_length=120)
    descricao: str | None = None
    ativo: bool = True


class VeiculoUpdate(Update):
    required_fields: ClassVar = ("identificador", "ativo")
    identificador: str | None = Field(default=None, min_length=1, max_length=80)
    placa: str | None = Field(default=None, min_length=1, max_length=20)
    modelo: str | None = Field(default=None, max_length=120)
    descricao: str | None = None
    ativo: bool | None = None


class VeiculoResponse(VeiculoCreate, Response):
    pass


class MotoristaCreate(Input):
    empresa_id: UUID
    nome: str = Field(min_length=1, max_length=150)
    documento: str | None = Field(default=None, min_length=1, max_length=40)
    telefone: str | None = Field(default=None, max_length=40)
    ativo: bool = True


class MotoristaUpdate(Update):
    required_fields: ClassVar = ("nome", "ativo")
    nome: str | None = Field(default=None, min_length=1, max_length=150)
    documento: str | None = Field(default=None, min_length=1, max_length=40)
    telefone: str | None = Field(default=None, max_length=40)
    ativo: bool | None = None


class MotoristaResponse(MotoristaCreate, Response):
    pass


class ViagemCreate(Input):
    transportadora_id: UUID
    veiculo_id: UUID
    motorista_id: UUID
    origem: str = Field(min_length=1, max_length=255)
    destino: str = Field(min_length=1, max_length=255)
    saida_em: AwareDatetime
    previsao_chegada_em: AwareDatetime | None = None
    observacoes: str | None = None


class ViagemUpdate(Update):
    required_fields: ClassVar = ("veiculo_id", "motorista_id", "origem", "destino", "saida_em", "status")
    veiculo_id: UUID | None = None
    motorista_id: UUID | None = None
    origem: str | None = Field(default=None, min_length=1, max_length=255)
    destino: str | None = Field(default=None, min_length=1, max_length=255)
    saida_em: AwareDatetime | None = None
    previsao_chegada_em: AwareDatetime | None = None
    inicio_real: AwareDatetime | None = None
    chegada_em: AwareDatetime | None = None
    status: StatusViagem | None = None
    observacoes: str | None = None


class ViagemResponse(Response):
    transportadora_id: UUID
    veiculo_id: UUID
    motorista_id: UUID
    origem: str
    destino: str
    saida_em: datetime
    previsao_chegada_em: datetime | None
    inicio_real: datetime | None
    chegada_em: datetime | None
    status: StatusViagem
    observacoes: str | None


class CargaCreate(Input):
    produto_id: UUID
    produtor_id: UUID
    cliente_id: UUID | None = None
    identificacao: str = Field(min_length=1, max_length=120)
    quantidade_caixas: int | None = Field(default=None, ge=0, le=2147483647)
    quantidade: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=4)
    unidade: str | None = Field(default=None, min_length=1, max_length=30)
    origem_produto: str | None = Field(default=None, max_length=255)
    observacoes: str | None = None


class CargaUpdate(Update):
    required_fields: ClassVar = ("identificacao", "status")
    identificacao: str | None = Field(default=None, min_length=1, max_length=120)
    quantidade_caixas: int | None = Field(default=None, ge=0, le=2147483647)
    quantidade: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=4)
    unidade: str | None = Field(default=None, min_length=1, max_length=30)
    origem_produto: str | None = Field(default=None, max_length=255)
    observacoes: str | None = None
    status: StatusCarga | None = None


class CargaResponse(CargaCreate, Response):
    viagem_id: UUID
    status: StatusCarga


class CaixaCreate(Input):
    identificacao: str = Field(min_length=1, max_length=120)
    codigo_externo: str | None = Field(default=None, max_length=120)
    peso: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=4)
    observacoes: str | None = None


class CaixaUpdate(Update):
    required_fields: ClassVar = ("identificacao", "status")
    identificacao: str | None = Field(default=None, min_length=1, max_length=120)
    codigo_externo: str | None = Field(default=None, max_length=120)
    peso: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=4)
    observacoes: str | None = None
    status: StatusCaixa | None = None


class CaixaResponse(CaixaCreate, Response):
    carga_id: UUID
    status: StatusCaixa
