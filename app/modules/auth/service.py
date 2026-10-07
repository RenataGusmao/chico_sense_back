import jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import DUMMY_HASH, create_access_token, decode_access_token, verify_password
from app.repositories.usuarios import UsuarioRepository
from app.repositories.empresas import EmpresaUsuarioRepository
from app.modules.auth.schemas import LoginRequest, TokenResponse, CurrentUserResponse
from app.schemas.usuarios import UsuarioResponse


def unauthorized() -> HTTPException:
    return HTTPException(401, "Credenciais invalidas.", headers={"WWW-Authenticate": "Bearer"})


class AuthService:
    def __init__(self, db: Session):
        self.users = UsuarioRepository(db)
        self.links = EmpresaUsuarioRepository(db)

    def login(self, data: LoginRequest) -> TokenResponse:
        user = self.users.by_email(str(data.email))
        valid = verify_password(data.senha.get_secret_value(), user.senha_hash if user and user.senha_hash else DUMMY_HASH)
        if not valid or not user or not user.ativo or not user.senha_hash:
            raise unauthorized()
        try:
            token = create_access_token(user.id)
        except RuntimeError as exc:
            raise HTTPException(503, "Autenticacao nao configurada.") from exc
        return TokenResponse(access_token=token, expires_in=settings.access_token_expire_minutes * 60)

    def current_user(self, token: str):
        try:
            user_id = decode_access_token(token)
        except jwt.InvalidTokenError as exc:
            raise unauthorized() from exc
        except RuntimeError as exc:
            raise HTTPException(503, "Autenticacao nao configurada.") from exc
        user = self.users.get(user_id)
        if user is None or not user.ativo:
            raise unauthorized()
        return user

    def describe(self, user) -> CurrentUserResponse:
        return CurrentUserResponse(
            **UsuarioResponse.model_validate(user).model_dump(),
            perfil=user.perfil.nome if user.perfil else None,
            empresas=self.links.companies(user.id),
        )
