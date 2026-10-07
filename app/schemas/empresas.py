from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import TipoEmpresa


class EmpresaCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=180)
    tipo: TipoEmpresa
    documento: str | None = Field(default=None, min_length=1, max_length=40)
    ativo: bool = True


class EmpresaUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=180)
    tipo: TipoEmpresa | None = None
    documento: str | None = Field(default=None, min_length=1, max_length=40)
    ativo: bool | None = None

    @model_validator(mode="after")
    def reject_null(self):
        if any(getattr(self, field) is None for field in self.model_fields_set - {"documento"}):
            raise ValueError("Only documento can be null")
        return self


class EmpresaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
    tipo: TipoEmpresa
    documento: str | None
    ativo: bool
    created_at: datetime
    updated_at: datetime


class VinculoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    empresa_id: UUID
    usuario_id: UUID
    ativo: bool
