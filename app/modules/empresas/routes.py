from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_database_session, get_current_user, require_profiles
from app.models.usuario import Usuario
from app.modules.empresas.service import EmpresaService
from app.schemas.empresas import EmpresaCreate, EmpresaUpdate, EmpresaResponse, VinculoResponse
from app.schemas.usuarios import UsuarioResponse

router = APIRouter(prefix="/api/v1/empresas", tags=["Empresas"])
admin = require_profiles("ADMIN")


@router.post("", response_model=EmpresaResponse, status_code=201, dependencies=[Depends(admin)])
def create(data: EmpresaCreate, db: Session = Depends(get_database_session)):
    return EmpresaService(db).create(data)


@router.get("", response_model=list[EmpresaResponse])
def companies(offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), user: Usuario = Depends(get_current_user), db: Session = Depends(get_database_session)):
    return EmpresaService(db).list(user, offset, limit)


@router.get("/{empresa_id}", response_model=EmpresaResponse)
def detail(empresa_id: UUID, user: Usuario = Depends(get_current_user), db: Session = Depends(get_database_session)):
    return EmpresaService(db).authorize(empresa_id, user)


@router.patch("/{empresa_id}", response_model=EmpresaResponse, dependencies=[Depends(admin)])
def update(empresa_id: UUID, data: EmpresaUpdate, db: Session = Depends(get_database_session)):
    return EmpresaService(db).update(empresa_id, data)


@router.post("/{empresa_id}/usuarios/{usuario_id}", response_model=VinculoResponse, dependencies=[Depends(admin)])
def link(empresa_id: UUID, usuario_id: UUID, db: Session = Depends(get_database_session)):
    return EmpresaService(db).link(empresa_id, usuario_id)


@router.get("/{empresa_id}/usuarios", response_model=list[UsuarioResponse], dependencies=[Depends(require_profiles("ADMIN", "GESTOR"))])
def users(empresa_id: UUID, offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), user: Usuario = Depends(get_current_user), db: Session = Depends(get_database_session)):
    return EmpresaService(db).users(empresa_id, user, offset, limit)
