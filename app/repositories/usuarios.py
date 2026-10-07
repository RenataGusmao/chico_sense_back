from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.usuario import Usuario, Perfil


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: UUID) -> Usuario | None:
        return self.db.get(Usuario, user_id)

    def by_email(self, email: str) -> Usuario | None:
        return self.db.scalar(select(Usuario).where(func.lower(func.trim(Usuario.email)) == email.strip().lower()))

    def list(self, offset: int, limit: int) -> list[Usuario]:
        return list(self.db.scalars(select(Usuario).order_by(Usuario.created_at, Usuario.id).offset(offset).limit(limit)))

    def add(self, user: Usuario) -> None:
        self.db.add(user)


class PerfilRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, profile_id: UUID) -> Perfil | None:
        return self.db.get(Perfil, profile_id)

    def by_name(self, name: str) -> Perfil | None:
        return self.db.scalar(select(Perfil).where(Perfil.nome == name))

    def list(self) -> list[Perfil]:
        return list(self.db.scalars(select(Perfil).order_by(Perfil.nome)))
