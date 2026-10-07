from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.models.usuario import EmpresaUsuario, Usuario
from app.repositories.empresas import EmpresaRepository, EmpresaUsuarioRepository
from app.repositories.usuarios import UsuarioRepository
from app.schemas.empresas import EmpresaCreate, EmpresaUpdate
from app.services.persistence import commit


def is_admin(user: Usuario) -> bool:
    return bool(user.perfil and user.perfil.nome == "ADMIN")


class EmpresaService:
    def __init__(self, db: Session):
        self.db = db
        self.companies = EmpresaRepository(db)
        self.links = EmpresaUsuarioRepository(db)

    def get(self, company_id: UUID) -> Empresa:
        company = self.companies.get(company_id)
        if company is None:
            raise HTTPException(404, "Empresa nao encontrada.")
        return company

    def authorize(self, company_id: UUID, user: Usuario) -> Empresa:
        if not is_admin(user):
            link = self.links.get(company_id, user.id)
            if not link or not link.ativo:
                raise HTTPException(403, "Acesso a empresa nao permitido.")
        company = self.get(company_id)
        if not is_admin(user) and not company.ativo:
            raise HTTPException(403, "Empresa inativa.")
        return company

    def list(self, user: Usuario, offset: int, limit: int):
        return self.companies.list(offset, limit, None if is_admin(user) else user.id)

    def create(self, data: EmpresaCreate) -> Empresa:
        company = Empresa(**data.model_dump())
        self.db.add(company)
        commit(self.db)
        self.db.refresh(company)
        return company

    def update(self, company_id: UUID, data: EmpresaUpdate) -> Empresa:
        company = self.get(company_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(company, key, value)
        commit(self.db)
        self.db.refresh(company)
        return company

    def link(self, company_id: UUID, user_id: UUID) -> EmpresaUsuario:
        self.get(company_id)
        if UsuarioRepository(self.db).get(user_id) is None:
            raise HTTPException(404, "Usuario nao encontrado.")
        link = self.links.get(company_id, user_id)
        if link is None:
            link = EmpresaUsuario(empresa_id=company_id, usuario_id=user_id, ativo=True)
            self.db.add(link)
        else:
            link.ativo = True
        commit(self.db)
        self.db.refresh(link)
        return link

    def users(self, company_id: UUID, actor: Usuario, offset: int, limit: int):
        self.authorize(company_id, actor)
        return self.links.users(company_id, offset, limit)
