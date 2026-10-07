from collections.abc import Generator

from sqlalchemy.orm import Session

from app.core.database import get_db
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.modules.auth.service import AuthService, unauthorized
from app.models.usuario import Usuario

bearer = HTTPBearer(auto_error=False)


def get_database_session() -> Generator[Session, None, None]:
    yield from get_db()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_database_session),
) -> Usuario:
    if credentials is None:
        raise unauthorized()
    return AuthService(db).current_user(credentials.credentials)


def require_profiles(*names: str):
    def dependency(user: Usuario = Depends(get_current_user)) -> Usuario:
        if not user.perfil or user.perfil.nome not in names:
            raise HTTPException(403, "Perfil sem permissao.")
        return user
    return dependency
