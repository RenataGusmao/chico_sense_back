"""Acquisition contracts: explicit operational controls, no ethylene result fields."""
from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID
from pydantic import AwareDatetime, Field, model_validator
from app.schemas.operacional import Input, Response


class SincronizacaoCreate(Input):
    chave_idempotencia: UUID
    origem_dados: Literal["THINGSPEAK", "BANCO"] = "THINGSPEAK"
    inicio: AwareDatetime | None = None
    fim: AwareDatetime | None = None
    complementar_encerrada: bool = Field(default=False, strict=True)
    justificativa: str | None = Field(default=None, min_length=1, max_length=2000)
    limite_atraso_s: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=3)
    max_requisicoes: int = Field(default=16, ge=1, le=32, strict=True)

    @model_validator(mode="after")
    def complemento_auditado(self):
        if self.complementar_encerrada and not self.justificativa:
            raise ValueError("Complementacao exige justificativa explicita.")
        if self.inicio and self.fim and self.fim < self.inicio:
            raise ValueError("Fim anterior ao inicio solicitado.")
        return self


class SincronizacaoResponse(Response):
    sessao_id: UUID
    usuario_id: UUID
    revisao: int
    chave_idempotencia: UUID
    origem_dados: str
    estado: str
    inicio_janela: datetime
    fim_janela: datetime
    iniciada_em: datetime
    finalizada_em: datetime | None
    expira_em: datetime
    complementacao: bool
    justificativa: str | None
    resumo: dict


class LeituraHistoricoResponse(Input):
    id: UUID
    fonte_id: UUID
    medicao_id: UUID | None
    sensor_id: UUID
    tipo: str
    channel_id: str
    field_name: str
    unidade: str
    entry_id: int
    medida_em: datetime
    timestamp_origem: str
    recebida_em: datetime | None
    processada_em: datetime
    valor: Decimal | None
    estado: str
    motivo: str | None
    revisao_incorporacao: int
    tardia: bool | None
    apos_encerramento: bool
    fora_de_ordem: bool
    conflito_observado: bool


class HistoricoResponse(Input):
    sessao_id: UUID
    estado_sessao: str
    revisao: int
    inicio: datetime
    fim: datetime
    massa_kg: Decimal
    maturacao: str
    total: int
    limit: int
    offset: int
    leituras: list[LeituraHistoricoResponse]
    metadados_temporais_invalidos: bool
    cancelada_para_analise: bool
    ocorrencias: list[dict]


class EstadoSincronizacaoResponse(Input):
    sessao_id: UUID
    revisao_disponivel: int
    em_execucao: UUID | None
    tentativas: list[SincronizacaoResponse]


class QualidadeResponse(Input):
    sessao_id: UUID
    revisao: int
    inicio: datetime
    fim: datetime
    intervalo_maximo_s: Decimal
    natureza: str
    metadados_temporais_invalidos: bool
    cancelada_para_analise: bool
    indicadores: list[dict]
    codigos_ocorrencias: list[str]
    limites: str
