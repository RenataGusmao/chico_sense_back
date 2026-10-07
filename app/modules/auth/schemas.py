from pydantic import BaseModel, EmailStr, SecretStr, Field

from app.schemas.usuarios import EmailInput, UsuarioResponse
from app.schemas.empresas import EmpresaResponse


class LoginRequest(EmailInput):
    email: EmailStr
    senha: SecretStr = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class CurrentUserResponse(UsuarioResponse):
    perfil: str | None
    empresas: list[EmpresaResponse]
