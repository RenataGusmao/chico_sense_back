from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.usuario import Usuario
from app.repositories.usuarios import UsuarioRepository, PerfilRepository
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate
from app.services.persistence import commit


class UsuarioService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UsuarioRepository(db)
        self.profiles = PerfilRepository(db)

    def get(self, user_id: UUID) -> Usuario:
        user = self.users.get(user_id)
        if user is None:
            raise HTTPException(404, "Usuario nao encontrado.")
        return user

    def create(self, data: UsuarioCreate) -> Usuario:
        if self.users.by_email(str(data.email)):
            raise HTTPException(409, "Email ja cadastrado.")
        if not self.profiles.get(data.perfil_id):
            raise HTTPException(404, "Perfil nao encontrado.")
        values = data.model_dump(exclude={"senha"})
        values["email"] = str(data.email).strip().lower()
        user = Usuario(**values, senha_hash=hash_password(data.senha.get_secret_value()))
        self.users.add(user)
        commit(self.db)
        self.db.refresh(user)
        return user

    def update(self, user_id: UUID, data: UsuarioUpdate) -> Usuario:
        user = self.get(user_id)
        values = data.model_dump(exclude_unset=True, exclude={"senha"})
        if "email" in values:
            values["email"] = str(values["email"]).strip().lower()
            existing = self.users.by_email(values["email"])
            if existing and existing.id != user.id:
                raise HTTPException(409, "Email ja cadastrado.")
        if "perfil_id" in values and not self.profiles.get(values["perfil_id"]):
            raise HTTPException(404, "Perfil nao encontrado.")
        for key, value in values.items():
            setattr(user, key, value)
        if data.senha is not None:
            user.senha_hash = hash_password(data.senha.get_secret_value())
        commit(self.db)
        self.db.refresh(user)
        return user

    def list(self, offset: int, limit: int) -> list[Usuario]:
        return self.users.list(offset, limit)

    def profiles_list(self):
        return self.profiles.list()
