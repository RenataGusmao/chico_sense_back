from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_database_session, get_current_user
from app.models.usuario import Usuario
from app.modules.auth.schemas import LoginRequest, TokenResponse, CurrentUserResponse
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_database_session)):
    return AuthService(db).login(data)


@router.get("/me", response_model=CurrentUserResponse)
def me(user: Usuario = Depends(get_current_user), db: Session = Depends(get_database_session)):
    return AuthService(db).describe(user)
