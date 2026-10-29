"""API contracts for declarations and sessions; independent of the math engine."""
from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from pydantic import AwareDatetime, Field
from app.schemas.operacional import Input, Response
from app.models.sessoes_monitoramento import MaturacaoCarga, StatusSessao

MassaKg = Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=4)]


class CargaMonitoramentoPut(Input):
    produto_identificado: Literal["MANGA_TOMMY_ATKINS"]
    massa_kg: MassaKg
    maturacao: MaturacaoCarga = MaturacaoCarga.DESCONHECIDA
    lote_codigo: str = Field(min_length=1, max_length=120)
    lote_hipotetico: bool = Field(strict=True)
    rastreabilidade: str = Field(min_length=1, max_length=2000)


class CargaMonitoramentoResponse(Response):
    carga_id: UUID
    produto_identificado: str
    massa_kg: Decimal
    maturacao: MaturacaoCarga
    lote_codigo: str
    lote_hipotetico: bool
    rastreabilidade: str
    versao: int
    atualizado_por_id: UUID


class SessaoCreate(Input):
    inicio: AwareDatetime
    sensor_temperatura_id: UUID
    sensor_umidade_id: UUID | None = None
    ambiente_aquisicao: Literal["LABORATORIO", "TRANSPORTE_REFRIGERADO"]
    chave_idempotencia: UUID
    observacoes: str | None = Field(default=None, max_length=2000)


class SessaoFinalizar(Input):
    fim: AwareDatetime
    motivo: str = Field(min_length=1, max_length=2000)


class SessaoResponse(Response):
    carga_id: UUID
    viagem_id: UUID
    configuracao_id: UUID
    inicio: datetime
    fim: datetime | None
    estado: StatusSessao
    sensor_temperatura_id: UUID
    sensor_umidade_id: UUID | None
    ambiente_aquisicao: str
    observacoes: str | None
    configuracao_versao: int
    produto_identificado: str
    massa_kg: Decimal
    maturacao: MaturacaoCarga
    lote_codigo: str
    lote_hipotetico: bool
    rastreabilidade: str
    origem_sensor: dict
    criada_por_id: UUID
    finalizada_por_id: UUID | None
    motivo_fim: str | None
    chave_idempotencia: UUID
