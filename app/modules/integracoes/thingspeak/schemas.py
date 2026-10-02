from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ThingSpeakChannelConfig(BaseModel):
    base_url: str
    channel_id: str | None = None
    read_api_key: str | None = None
    timeout_seconds: float = 10


class ThingSpeakChannelMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int
    name: str | None = None
    description: str | None = None


class ThingSpeakFeed(BaseModel):
    created_at: datetime
    entry_id: int
    fields: dict[str, str | None] = Field(default_factory=dict)
    raw: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api_payload(cls, payload: dict[str, Any]) -> "ThingSpeakFeed":
        fields = {
            key: value
            for key, value in payload.items()
            if key.startswith("field") and key.removeprefix("field").isdigit()
        }
        return cls(
            created_at=payload["created_at"],
            entry_id=payload["entry_id"],
            fields=fields,
            raw=payload,
        )


class ThingSpeakFeedsResponse(BaseModel):
    channel: ThingSpeakChannelMetadata | None = None
    feeds: list[ThingSpeakFeed] = Field(default_factory=list)


class ThingSpeakFieldMapping(BaseModel):
    sensor_id: UUID | None = None
    tipo: str | None = None
    contexto: str | None = None
    unidade: str | None = None
    viagem_id: UUID | None = None
    carga_id: UUID | None = None
    caixa_id: UUID | None = None


class ThingSpeakMappingConfig(BaseModel):
    fields: dict[str, ThingSpeakFieldMapping] = Field(default_factory=dict)

    @classmethod
    def from_raw_mapping(cls, raw_mapping: dict[str, Any] | None) -> "ThingSpeakMappingConfig":
        if not raw_mapping:
            return cls()
        return cls(fields=raw_mapping)


class NormalizedThingSpeakReading(BaseModel):
    source: str = "thingspeak"
    channel_id: str
    entry_id: int
    field_name: str
    created_at: datetime
    sensor_id: UUID | None = None
    tipo: str | None = None
    contexto: str | None = None
    valor: Decimal | None = None
    unidade: str | None = None
    viagem_id: UUID | None = None
    carga_id: UUID | None = None
    caixa_id: UUID | None = None
    valor_original: str | None = None
    ignorada: bool = False
    motivo_ignorada: str | None = None

    @field_validator("valor", mode="before")
    @classmethod
    def parse_decimal(cls, value: Any) -> Decimal | None:
        if value is None or value == "":
            return None
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            return None


class ThingSpeakMappingResult(BaseModel):
    channel_id: str
    feeds_processados: int
    leituras_normalizadas: list[NormalizedThingSpeakReading] = Field(default_factory=list)
    ignorados: int = 0


class ThingSpeakSyncError(BaseModel):
    entry_id: int
    field_name: str
    motivo: str


class ThingSpeakSyncSummary(BaseModel):
    feeds_recebidos: int
    fields_processados: int
    medicoes_criadas: int
    duplicados: int
    ignorados: int
    erros: list[ThingSpeakSyncError] = Field(default_factory=list)


class ThingSpeakStatusResponse(BaseModel):
    configured: bool
    base_url: str
    channel_id: str | None = None
    message: str
