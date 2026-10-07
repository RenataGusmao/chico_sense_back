from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_database_session, require_profiles
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse, PerfilResponse
from app.services.usuarios import UsuarioService

router = APIRouter(prefix="/api/v1", tags=["Usuarios"], dependencies=[Depends(require_profiles("ADMIN"))])


@router.get("/perfis", response_model=list[PerfilResponse])
def profiles(db: Session = Depends(get_database_session)):
    return UsuarioService(db).profiles_list()


@router.post("/usuarios", response_model=UsuarioResponse, status_code=201)
def create(data: UsuarioCreate, db: Session = Depends(get_database_session)):
    return UsuarioService(db).create(data)


@router.get("/usuarios", response_model=list[UsuarioResponse])
def users(offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_database_session)):
    return UsuarioService(db).list(offset, limit)


@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def detail(usuario_id: UUID, db: Session = Depends(get_database_session)):
    return UsuarioService(db).get(usuario_id)


@router.patch("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def update(usuario_id: UUID, data: UsuarioUpdate, db: Session = Depends(get_database_session)):
    return UsuarioService(db).update(usuario_id, data)
