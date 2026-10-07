from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.empresa import Empresa


class Perfil(ModelBase, Base):
    __tablename__ = "perfis"

    nome: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)

    usuarios: Mapped[list[Usuario]] = relationship(back_populates="perfil")


class Usuario(ModelBase, Base):
    __tablename__ = "usuarios"

    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    senha_hash: Mapped[str | None] = mapped_column(String(255))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    perfil_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("perfis.id"),
    )

    perfil: Mapped[Perfil | None] = relationship(back_populates="usuarios")
    empresas: Mapped[list[EmpresaUsuario]] = relationship(back_populates="usuario")

    __table_args__ = (
        Index("uq_usuarios_email_normalizado", func.lower(func.trim(email)), unique=True),
    )


class EmpresaUsuario(ModelBase, Base):
    __tablename__ = "empresas_usuarios"
    __table_args__ = (
        UniqueConstraint("empresa_id", "usuario_id", name="uq_empresa_usuario"),
    )

    empresa_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("empresas.id"),
        nullable=False,
    )
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id"),
        nullable=False,
    )
    cargo: Mapped[str | None] = mapped_column(String(120))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    empresa: Mapped[Empresa] = relationship(back_populates="usuarios")
    usuario: Mapped[Usuario] = relationship(back_populates="empresas")
