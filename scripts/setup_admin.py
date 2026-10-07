"""Create initial profiles and administrator without resetting existing accounts."""
import argparse
import getpass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session

import app.models
from app.core.database import SessionLocal
from app.models.usuario import Perfil
from app.repositories.usuarios import PerfilRepository, UsuarioRepository
from app.schemas.usuarios import UsuarioCreate
from app.services.usuarios import UsuarioService
from app.services.persistence import commit


def setup_admin(db: Session, nome: str, email: str, senha: str | None = None):
    profiles = PerfilRepository(db)
    for name in ("ADMIN", "GESTOR", "OPERADOR", "CONSULTA"):
        if profiles.by_name(name) is None:
            db.add(Perfil(nome=name))
            db.flush()
    admin = profiles.by_name("ADMIN")
    existing = UsuarioRepository(db).by_email(email)
    if existing:
        if existing.perfil_id != admin.id or not existing.ativo:
            db.rollback()
            raise ValueError("Email existente nao pertence a um administrador ativo.")
        commit(db)
        return existing, False
    if senha is None:
        senha = getpass.getpass("Senha do administrador (minimo 12 caracteres): ")
    data = UsuarioCreate(nome=nome, email=email, senha=senha, perfil_id=admin.id)
    return UsuarioService(db).create(data), True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nome", required=True)
    parser.add_argument("--email", required=True)
    args = parser.parse_args()
    try:
        with SessionLocal() as db:
            user, created = setup_admin(db, args.nome, args.email)
            print(f"Administrador {'criado' if created else 'reutilizado'}: {user.id}")
    except Exception:
        # Validation exceptions may contain raw input; never print them here.
        print("Setup falhou. Confira email, senha, perfis e conexao com o banco.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
