from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

import app.models
from app.api.deps import get_database_session
from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.main import create_app
from app.models.usuario import Usuario, Perfil, EmpresaUsuario
from app.models.empresa import Empresa
from app.schemas.usuarios import UsuarioCreate
from app.services.usuarios import UsuarioService
from scripts.setup_admin import setup_admin

PASSWORD = "test-only-password-123"


@pytest.fixture
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    for model in (Perfil, Usuario, Empresa, EmpresaUsuario):
        model.__table__.create(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture
def client(db, monkeypatch):
    monkeypatch.setattr(settings, "secret_key", "test-only-signing-key-never-use-in-production")
    application = create_app()
    def override():
        yield db
    application.dependency_overrides[get_database_session] = override
    with TestClient(application) as test_client:
        yield test_client


@pytest.fixture
def admin(db):
    return setup_admin(db, "Admin", "admin@example.com", PASSWORD)[0]


def headers(user):
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


def company(client, admin, tipo="PRODUTOR"):
    response = client.post("/api/v1/empresas", headers=headers(admin), json={"nome": "Empresa teste", "tipo": tipo})
    assert response.status_code == 201
    return response.json()


def new_user(db, role="CONSULTA", email="reader@example.com"):
    profile = db.scalar(select(Perfil).where(Perfil.nome == role))
    return UsuarioService(db).create(UsuarioCreate(nome="Leitor", email=email, senha=PASSWORD, perfil_id=profile.id))


def test_password_hash():
    hashed = hash_password(PASSWORD)
    assert hashed != PASSWORD
    assert hashed.startswith("$argon2id$")
    assert verify_password(PASSWORD, hashed)
    assert not verify_password("incorrect", hashed)


def test_invalid_hash():
    assert not verify_password(PASSWORD, "not-a-hash")


def test_create_user(client, admin, db):
    profile = db.scalar(select(Perfil).where(Perfil.nome == "GESTOR"))
    response = client.post("/api/v1/usuarios", headers=headers(admin),
                           json={"nome": "Gestor", "email": " GESTOR@EXAMPLE.COM ", "senha": PASSWORD, "perfil_id": str(profile.id)})
    assert response.status_code == 201
    assert response.json()["email"] == "gestor@example.com"
    assert "senha_hash" not in response.text
    assert "password_hash" not in response.text
    assert PASSWORD not in response.text


def test_email_unique(client, admin):
    response = client.post("/api/v1/usuarios", headers=headers(admin),
                           json={"nome": "Outro", "email": "ADMIN@EXAMPLE.COM", "senha": PASSWORD, "perfil_id": str(admin.perfil_id)})
    assert response.status_code == 409


def test_database_email_identity(db, admin):
    from sqlalchemy.exc import IntegrityError
    db.add(Usuario(nome="Duplicate", email=" ADMIN@EXAMPLE.COM "))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_valid_login(client, admin):
    response = client.post("/api/v1/auth/login", json={"email": "ADMIN@EXAMPLE.COM", "senha": PASSWORD})
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert decode_access_token(response.json()["access_token"]) == admin.id


@pytest.mark.parametrize("email,password", [("missing@example.com", PASSWORD), ("admin@example.com", "wrong")])
def test_invalid_login(client, admin, email, password):
    response = client.post("/api/v1/auth/login", json={"email": email, "senha": password})
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais invalidas."


def test_inactive_login(client, admin, db):
    admin.ativo = False
    db.commit()
    assert client.post("/api/v1/auth/login", json={"email": admin.email, "senha": PASSWORD}).status_code == 401
    assert client.get("/api/v1/auth/me", headers=headers(admin)).status_code == 401


def test_jwt_creation(client, admin):
    assert decode_access_token(create_access_token(admin.id)) == admin.id


@pytest.mark.parametrize("kind", ["expired", "tampered", "algorithm", "missing", "subject", "audience", "type"])
def test_invalid_jwt(client, admin, kind):
    payload = {"sub": str(admin.id), "iat": datetime.now(timezone.utc),
               "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
               "iss": "chicosense-api", "aud": "chicosense-api", "type": "access"}
    if kind == "expired":
        payload["exp"] = datetime.now(timezone.utc) - timedelta(seconds=10)
    if kind == "missing":
        del payload["exp"]
    if kind == "subject":
        payload["sub"] = "not-a-uuid"
    if kind == "audience":
        payload["aud"] = "other-service"
    if kind == "type":
        payload["type"] = "refresh"
    token = jwt.encode(payload, "wrong-test-key" if kind == "tampered" else settings.secret_key,
                       algorithm="HS384" if kind == "algorithm" else "HS256")
    assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_me_without_token(client):
    assert client.get("/api/v1/auth/me").status_code == 401


def test_me_multi_company(client, admin, db):
    user = new_user(db)
    ids = []
    for tipo in ("PRODUTOR", "TRANSPORTADORA"):
        data = company(client, admin, tipo)
        ids.append(data["id"])
        assert client.post(f"/api/v1/empresas/{data['id']}/usuarios/{user.id}", headers=headers(admin)).status_code == 200
    response = client.get("/api/v1/auth/me", headers=headers(user))
    assert response.status_code == 200
    assert response.json()["perfil"] == "CONSULTA"
    assert {c["id"] for c in response.json()["empresas"]} == set(ids)
    assert "senha_hash" not in response.text
    assert "password_hash" not in response.text


@pytest.mark.parametrize("tipo", ["PRODUTOR", "TRANSPORTADORA", "CLIENTE"])
def test_company_types(client, admin, tipo):
    assert company(client, admin, tipo)["tipo"] == tipo


def test_invalid_company_type(client, admin):
    assert client.post("/api/v1/empresas", headers=headers(admin), json={"nome": "Teste", "tipo": "LOGISTICA"}).status_code == 422


def test_link_idempotent(client, admin, db):
    user = new_user(db)
    data = company(client, admin)
    path = f"/api/v1/empresas/{data['id']}/usuarios/{user.id}"
    first = client.post(path, headers=headers(admin))
    second = client.post(path, headers=headers(admin))
    assert first.json()["id"] == second.json()["id"]
    assert db.scalar(select(func.count()).select_from(EmpresaUsuario)) == 1


def test_lists_and_detail(client, admin):
    data = company(client, admin)
    assert client.get("/api/v1/usuarios", headers=headers(admin)).json()[0]["id"] == str(admin.id)
    assert client.get(f"/api/v1/usuarios/{admin.id}", headers=headers(admin)).status_code == 200
    assert client.get("/api/v1/empresas", headers=headers(admin)).json()[0]["id"] == data["id"]
    assert client.get(f"/api/v1/empresas/{data['id']}", headers=headers(admin)).status_code == 200
    assert len(client.get("/api/v1/perfis", headers=headers(admin)).json()) == 4


def test_logical_deactivation(client, admin, db):
    user = new_user(db)
    response = client.patch(f"/api/v1/usuarios/{user.id}", headers=headers(admin), json={"ativo": False})
    assert response.status_code == 200
    assert response.json()["ativo"] is False
    assert db.get(Usuario, user.id) is not None


@pytest.mark.parametrize("role", ["GESTOR", "OPERADOR", "CONSULTA"])
def test_non_admin_forbidden(client, admin, db, role):
    user = new_user(db, role)
    assert client.get("/api/v1/usuarios", headers=headers(user)).status_code == 403
    assert client.post("/api/v1/empresas", headers=headers(user), json={"nome": "Teste", "tipo": "CLIENTE"}).status_code == 403
    assert client.patch(f"/api/v1/usuarios/{user.id}", headers=headers(user), json={"perfil_id": str(admin.perfil_id)}).status_code == 403


def test_company_isolation(client, admin, db):
    user = new_user(db, "GESTOR")
    owned = company(client, admin)
    other = company(client, admin)
    client.post(f"/api/v1/empresas/{owned['id']}/usuarios/{user.id}", headers=headers(admin))
    assert [item["id"] for item in client.get("/api/v1/empresas", headers=headers(user)).json()] == [owned["id"]]
    assert client.get(f"/api/v1/empresas/{other['id']}", headers=headers(user)).status_code == 403
    assert client.get(f"/api/v1/empresas/{owned['id']}/usuarios", headers=headers(user)).status_code == 200
    assert client.get(f"/api/v1/empresas/{other['id']}/usuarios", headers=headers(user)).status_code == 403


def test_inactive_membership(client, admin, db):
    user = new_user(db)
    data = company(client, admin)
    client.post(f"/api/v1/empresas/{data['id']}/usuarios/{user.id}", headers=headers(admin))
    link = db.scalar(select(EmpresaUsuario))
    link.ativo = False
    db.commit()
    assert client.get("/api/v1/auth/me", headers=headers(user)).json()["empresas"] == []
    assert client.get(f"/api/v1/empresas/{data['id']}", headers=headers(user)).status_code == 403


def test_setup_admin_idempotent(db):
    first, created = setup_admin(db, "Admin", "admin@example.com", PASSWORD)
    original_hash = first.senha_hash
    second, created_again = setup_admin(db, "Changed", "ADMIN@EXAMPLE.COM", "unused")
    assert created is True and created_again is False
    assert first.id == second.id
    assert second.senha_hash == original_hash
    assert db.scalar(select(func.count()).select_from(Usuario)) == 1
    assert db.scalar(select(func.count()).select_from(Perfil)) == 4


def test_setup_does_not_promote_existing_user(db, admin):
    user = new_user(db)
    with pytest.raises(ValueError):
        setup_admin(db, "Admin", user.email, PASSWORD)


def test_placeholder_key_rejected(client, admin, monkeypatch):
    monkeypatch.setattr(settings, "secret_key", "change-this-secret-key")
    assert client.post("/api/v1/auth/login", json={"email": admin.email, "senha": PASSWORD}).status_code == 503


def test_patch_company(client, admin):
    data = company(client, admin)
    response = client.patch(f"/api/v1/empresas/{data['id']}", headers=headers(admin), json={"nome": "Atualizada", "ativo": False})
    assert response.status_code == 200
    assert response.json()["nome"] == "Atualizada"
    assert response.json()["ativo"] is False


def test_missing_records(client, admin):
    assert client.get(f"/api/v1/usuarios/{uuid4()}", headers=headers(admin)).status_code == 404
    assert client.get(f"/api/v1/empresas/{uuid4()}", headers=headers(admin)).status_code == 404


def test_patch_user_password_email(client, admin, db):
    user = new_user(db)
    response = client.patch(f"/api/v1/usuarios/{user.id}", headers=headers(admin),
                            json={"email": " UPDATED@EXAMPLE.COM ", "senha": "new-test-password-123"})
    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"
    assert verify_password("new-test-password-123", db.get(Usuario, user.id).senha_hash)


def test_patch_explicit_null_rejected(client, admin):
    assert client.patch(f"/api/v1/usuarios/{admin.id}", headers=headers(admin), json={"ativo": None}).status_code == 422


def test_validation_does_not_expose_password(client, admin):
    secret_input = "s3cr3t"
    response = client.post("/api/v1/usuarios", headers=headers(admin),
                           json={"nome": "Teste", "email": "bad-email", "senha": secret_input,
                                 "perfil_id": str(admin.perfil_id)})
    assert response.status_code == 422
    assert secret_input not in response.text
    assert all("input" not in error and "ctx" not in error for error in response.json()["detail"])


def test_inactive_company_excluded(client, admin, db):
    user = new_user(db)
    data = company(client, admin)
    client.post(f"/api/v1/empresas/{data['id']}/usuarios/{user.id}", headers=headers(admin))
    client.patch(f"/api/v1/empresas/{data['id']}", headers=headers(admin), json={"ativo": False})
    assert client.get("/api/v1/empresas", headers=headers(user)).json() == []
    assert client.get("/api/v1/auth/me", headers=headers(user)).json()["empresas"] == []
    assert client.get(f"/api/v1/empresas/{data['id']}", headers=headers(user)).status_code == 403


def test_missing_profile(client, admin):
    response = client.post("/api/v1/usuarios", headers=headers(admin),
                           json={"nome": "Teste", "email": "other@example.com", "senha": PASSWORD,
                                 "perfil_id": str(uuid4())})
    assert response.status_code == 404


def test_duplicate_email_update(client, admin, db):
    user = new_user(db)
    response = client.patch(f"/api/v1/usuarios/{user.id}", headers=headers(admin), json={"email": "ADMIN@EXAMPLE.COM"})
    assert response.status_code == 409
