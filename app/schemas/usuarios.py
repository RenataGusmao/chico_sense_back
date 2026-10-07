from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator, model_validator


class EmailInput(BaseModel):
    @field_validator("email", mode="before", check_fields=False)
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower() if isinstance(value, str) else value


class UsuarioCreate(EmailInput):
    nome: str = Field(min_length=1, max_length=150)
    email: EmailStr = Field(max_length=255)
    senha: SecretStr = Field(min_length=12, max_length=128)
    perfil_id: UUID
    ativo: bool = True


class UsuarioUpdate(EmailInput):
    nome: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = Field(default=None, max_length=255)
    senha: SecretStr | None = Field(default=None, min_length=12, max_length=128)
    perfil_id: UUID | None = None
    ativo: bool | None = None

    @model_validator(mode="after")
    def reject_null(self):
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Explicit null values are not supported")
        return self


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
    email: str
    perfil_id: UUID | None
    ativo: bool
    created_at: datetime
    updated_at: datetime


class PerfilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
    descricao: str | None
