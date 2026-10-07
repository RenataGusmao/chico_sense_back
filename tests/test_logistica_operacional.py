from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

import app.models
from app.api.deps import get_database_session
from app.main import create_app
from app.models.empresa import Empresa
from app.models.enums import TipoEmpresa
from app.models.produto import Produto, ParametroProduto
from app.models.logistica import Veiculo, Motorista, Viagem, Carga, Caixa

DATE = "2026-10-07T12:00:00Z"


@pytest.fixture
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    @event.listens_for(engine, "connect")
    def enforce_foreign_keys(connection, record):
        connection.execute("PRAGMA foreign_keys=ON")
    for model in (Empresa, Produto, ParametroProduto, Veiculo, Motorista, Viagem, Carga, Caixa):
        model.__table__.create(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture
def client(db):
    application = create_app()
    def override():
        yield db
    application.dependency_overrides[get_database_session] = override
    with TestClient(application) as test_client:
        yield test_client


def post(client, path, payload):
    response = client.post("/api/v1" + path, json=payload)
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
def world(client, db):
    companies = {
        "transportadora": Empresa(nome="Transportadora teste", tipo=TipoEmpresa.TRANSPORTADORA, ativo=True),
        "produtor": Empresa(nome="Produtor teste", tipo=TipoEmpresa.PRODUTOR, ativo=True),
        "cliente": Empresa(nome="Cliente teste", tipo=TipoEmpresa.CLIENTE, ativo=True),
    }
    db.add_all(companies.values())
    db.commit()
    ids = {key: str(value.id) for key, value in companies.items()}
    product = post(client, "/produtos", {"nome": "Produto teste"})
    vehicle = post(client, "/veiculos", {"empresa_id": ids["transportadora"], "identificador": "V-1"})
    driver = post(client, "/motoristas", {"empresa_id": ids["transportadora"], "nome": "Motorista teste"})
    trip = post(client, "/viagens", {"transportadora_id": ids["transportadora"], "veiculo_id": vehicle["id"],
                 "motorista_id": driver["id"], "origem": "Origem teste", "destino": "Destino teste", "saida_em": DATE})
    cargo = post(client, f"/viagens/{trip['id']}/cargas", {"produto_id": product["id"],
                 "produtor_id": ids["produtor"], "cliente_id": ids["cliente"], "identificacao": "C-1"})
    box = post(client, f"/cargas/{cargo['id']}/caixas", {"identificacao": "CX-1"})
    return ids | {"produtos": product, "veiculos": vehicle, "motoristas": driver,
                  "viagens": trip, "cargas": cargo, "caixas": box}


@pytest.mark.parametrize("resource", ["produtos", "veiculos", "motoristas", "viagens", "cargas", "caixas"])
def test_creation_and_detail(client, world, resource):
    response = client.get(f"/api/v1/{resource}/{world[resource]['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == world[resource]["id"]
    assert "created_at" in response.json()


@pytest.mark.parametrize("resource", ["produtos", "veiculos", "motoristas", "viagens", "cargas", "caixas"])
def test_missing_record(client, resource):
    assert client.get(f"/api/v1/{resource}/{uuid4()}").status_code == 404


@pytest.mark.parametrize("resource", ["produtos", "veiculos", "motoristas", "viagens"])
def test_lists(client, world, resource):
    assert client.get(f"/api/v1/{resource}").json()[0]["id"] == world[resource]["id"]


@pytest.mark.parametrize("resource,data", [
    ("produtos", {"nome": "Atualizado", "ativo": False}),
    ("veiculos", {"descricao": "Atualizado", "ativo": False}),
    ("motoristas", {"telefone": "teste", "ativo": False}),
    ("viagens", {"destino": "Atualizado"}),
    ("cargas", {"quantidade": "10.5000", "unidade": "unidade-teste"}),
    ("caixas", {"peso": "1.5000", "codigo_externo": "codigo-teste"}),
])
def test_updates(client, world, resource, data):
    response = client.patch(f"/api/v1/{resource}/{world[resource]['id']}", json=data)
    assert response.status_code == 200
    for field, value in data.items():
        if field in ("peso", "quantidade"):
            from decimal import Decimal
            assert Decimal(response.json()[field]) == Decimal(value)
        else:
            assert response.json()[field] == value


def test_parameter_has_no_default_scientific_values(client, world):
    path = f"/produtos/{world['produtos']['id']}/parametros"
    parameter = post(client, path, {"nome_parametro": "temperatura"})
    assert parameter["valor_minimo"] is None and parameter["valor_maximo"] is None
    assert len(client.get("/api/v1" + path).json()) == 1
    response = client.patch(f"/api/v1{path}/{parameter['id']}",
                            json={"valor_minimo": "1", "valor_maximo": "2", "observacao": "Valores sinteticos de teste"})
    assert response.status_code == 200


def test_parameter_merged_range_validation(client, world):
    path = f"/produtos/{world['produtos']['id']}/parametros"
    parameter = post(client, path, {"nome_parametro": "referencia", "valor_minimo": "1", "valor_maximo": "2"})
    assert client.patch(f"/api/v1{path}/{parameter['id']}", json={"valor_minimo": "3"}).status_code == 422


def test_parameter_wrong_product(client, world):
    parameter = post(client, f"/produtos/{world['produtos']['id']}/parametros", {"nome_parametro": "teste"})
    other = post(client, "/produtos", {"nome": "Outro produto"})
    assert client.patch(f"/api/v1/produtos/{other['id']}/parametros/{parameter['id']}", json={"unidade": "teste"}).status_code == 404


@pytest.mark.parametrize("resource", ["veiculos", "motoristas"])
def test_nonexistent_company(client, resource):
    data = {"empresa_id": str(uuid4()), "identificador": "V-2"} if resource == "veiculos" else {"empresa_id": str(uuid4()), "nome": "Teste"}
    assert client.post(f"/api/v1/{resource}", json=data).status_code == 404


@pytest.mark.parametrize("resource", ["veiculos", "motoristas"])
def test_company_filter(client, world, resource):
    assert len(client.get(f"/api/v1/{resource}", params={"empresa_id": world["transportadora"]}).json()) == 1
    assert client.get(f"/api/v1/{resource}", params={"empresa_id": world["produtor"]}).json() == []


@pytest.mark.parametrize("field", ["veiculo_id", "motorista_id", "transportadora_id"])
def test_missing_trip_reference(client, world, field):
    data = {"transportadora_id": world["transportadora"], "veiculo_id": world["veiculos"]["id"],
            "motorista_id": world["motoristas"]["id"], "origem": "O", "destino": "D", "saida_em": DATE}
    data[field] = str(uuid4())
    assert client.post("/api/v1/viagens", json=data).status_code == 404


def test_trip_status_transitions(client, world):
    path = f"/api/v1/viagens/{world['viagens']['id']}"
    response = client.patch(path, json={"status": "EM_ANDAMENTO"})
    assert response.status_code == 200 and response.json()["inicio_real"] is not None
    assert len(client.get("/api/v1/viagens", params={"status": "EM_ANDAMENTO"}).json()) == 1
    assert client.get("/api/v1/viagens", params={"status": "PLANEJADA"}).json() == []
    response = client.patch(path, json={"status": "CONCLUIDA"})
    assert response.status_code == 200 and response.json()["chegada_em"] is not None
    assert client.patch(path, json={"status": "EM_ANDAMENTO"}).status_code == 422


def test_trip_cancellation(client, world):
    path = f"/api/v1/viagens/{world['viagens']['id']}"
    assert client.patch(path, json={"status": "CANCELADA"}).status_code == 200
    assert client.patch(path, json={"status": "EM_ANDAMENTO"}).status_code == 422


def test_skipping_trip_status_rejected(client, world):
    assert client.patch(f"/api/v1/viagens/{world['viagens']['id']}", json={"status": "CONCLUIDA"}).status_code == 422


def test_trip_company_mismatch(client, world, db):
    other = Empresa(nome="Outra transportadora", tipo=TipoEmpresa.TRANSPORTADORA, ativo=True)
    db.add(other)
    db.commit()
    driver = post(client, "/motoristas", {"empresa_id": str(other.id), "nome": "Outro"})
    assert client.patch(f"/api/v1/viagens/{world['viagens']['id']}", json={"motorista_id": driver["id"]}).status_code == 422


def test_inactive_vehicle_trip_start(client, world):
    client.patch(f"/api/v1/veiculos/{world['veiculos']['id']}", json={"ativo": False})
    assert client.patch(f"/api/v1/viagens/{world['viagens']['id']}", json={"status": "EM_ANDAMENTO"}).status_code == 422


@pytest.mark.parametrize("field", ["viagem_id", "produto_id"])
def test_missing_cargo_reference(client, world, field):
    trip_id = str(uuid4()) if field == "viagem_id" else world["viagens"]["id"]
    data = {"produto_id": str(uuid4()) if field == "produto_id" else world["produtos"]["id"],
            "produtor_id": world["produtor"], "identificacao": "C-2"}
    assert client.post(f"/api/v1/viagens/{trip_id}/cargas", json=data).status_code == 404


def test_list_cargos_filters(client, world):
    path = f"/api/v1/viagens/{world['viagens']['id']}/cargas"
    assert client.get(path, params={"produto_id": world["produtos"]["id"], "status": "PLANEJADA"}).json()[0]["id"] == world["cargas"]["id"]
    assert client.get(path, params={"produto_id": str(uuid4())}).json() == []


def test_missing_box_parent(client):
    assert client.post(f"/api/v1/cargas/{uuid4()}/caixas", json={"identificacao": "CX"}).status_code == 404


def test_list_boxes(client, world):
    assert client.get(f"/api/v1/cargas/{world['cargas']['id']}/caixas").json()[0]["id"] == world["caixas"]["id"]


def test_relationships(client, world, db):
    trip = db.get(Viagem, UUID(world["viagens"]["id"]))
    cargo = trip.cargas[0]
    assert cargo.id == UUID(world["cargas"]["id"])
    assert cargo.caixas[0].id == UUID(world["caixas"]["id"])
    assert cargo.produto.cargas[0].id == cargo.id
    assert trip.veiculo.empresa.id == trip.transportadora_id
    assert trip.motorista.empresa.id == trip.transportadora_id


@pytest.mark.parametrize("kind", ["vehicle", "cargo", "box", "parameter"])
def test_scoped_duplicates(client, world, kind):
    if kind == "vehicle":
        path, data = "/veiculos", {"empresa_id": world["transportadora"], "identificador": "V-1"}
    elif kind == "cargo":
        path, data = f"/viagens/{world['viagens']['id']}/cargas", {"produto_id": world["produtos"]["id"], "produtor_id": world["produtor"], "identificacao": "C-1"}
    elif kind == "box":
        path, data = f"/cargas/{world['cargas']['id']}/caixas", {"identificacao": "CX-1"}
    else:
        path, data = f"/produtos/{world['produtos']['id']}/parametros", {"nome_parametro": "teste"}
        post(client, path, data)
    assert client.post("/api/v1" + path, json=data).status_code == 409
    assert client.get("/health").status_code == 200


def test_same_identifier_different_scope(client, world):
    second = post(client, f"/viagens/{world['viagens']['id']}/cargas",
                  {"produto_id": world["produtos"]["id"], "produtor_id": world["produtor"], "identificacao": "C-2"})
    assert post(client, f"/cargas/{second['id']}/caixas", {"identificacao": "CX-1"})["id"] != world["caixas"]["id"]


def test_cargo_and_box_status_coherence(client, world):
    cargo = f"/api/v1/cargas/{world['cargas']['id']}"
    box = f"/api/v1/caixas/{world['caixas']['id']}"
    assert client.patch(cargo, json={"status": "EM_TRANSITO"}).status_code == 422
    assert client.patch(box, json={"status": "EM_TRANSITO"}).status_code == 422
    client.patch(f"/api/v1/viagens/{world['viagens']['id']}", json={"status": "EM_ANDAMENTO"})
    assert client.patch(cargo, json={"status": "EM_TRANSITO"}).status_code == 200
    assert client.patch(box, json={"status": "EM_TRANSITO"}).status_code == 200
    assert client.patch(box, json={"status": "ENTREGUE"}).status_code == 200
    assert client.patch(cargo, json={"status": "ENTREGUE"}).status_code == 200
    assert client.patch(box, json={"status": "REGISTRADA"}).status_code == 422
    assert client.patch(cargo, json={"status": "PLANEJADA"}).status_code == 422


def test_no_reparenting_or_physical_delete(client, world):
    path = f"/api/v1/cargas/{world['cargas']['id']}"
    assert client.patch(path, json={"viagem_id": str(uuid4())}).status_code == 422
    assert client.delete(path).status_code == 405


@pytest.mark.parametrize("data", [{"peso": "-1"}, {"peso": "NaN"}, {"identificacao": None}, {"identificacao": "   "}])
def test_invalid_box_input(client, world, data):
    assert client.patch(f"/api/v1/caixas/{world['caixas']['id']}", json=data).status_code == 422


def test_quantity_requires_unit(client, world):
    assert client.patch(f"/api/v1/cargas/{world['cargas']['id']}", json={"quantidade": "1"}).status_code == 422


def test_trip_time_order(client, world):
    assert client.patch(f"/api/v1/viagens/{world['viagens']['id']}", json={"previsao_chegada_em": "2026-10-06T12:00:00Z"}).status_code == 422


def test_pagination(client, world):
    post(client, "/produtos", {"nome": "Outro"})
    assert len(client.get("/api/v1/produtos", params={"limit": 1}).json()) == 1
    assert len(client.get("/api/v1/produtos", params={"limit": 1, "offset": 1}).json()) == 1
    assert client.get("/api/v1/produtos", params={"limit": 101}).status_code == 422


def test_prototype_measurement_nullable_unchanged():
    from app.models.iot import Medicao
    assert Medicao.__table__.c.viagem_id.nullable
    assert Medicao.__table__.c.carga_id.nullable
    assert Medicao.__table__.c.caixa_id.nullable


def test_legacy_trip_can_receive_notes(client, world, db):
    from app.models.enums import StatusViagem
    trip = db.get(Viagem, UUID(world["viagens"]["id"]))
    trip.status = StatusViagem.CONCLUIDA
    trip.inicio_real = None
    db.commit()
    response = client.patch(f"/api/v1/viagens/{trip.id}", json={"observacoes": "Historico preservado"})
    assert response.status_code == 200
    assert response.json()["inicio_real"] is None


def test_new_cargo_in_closed_trip_rejected(client, world):
    client.patch(f"/api/v1/viagens/{world['viagens']['id']}", json={"status": "CANCELADA"})
    response = client.post(f"/api/v1/viagens/{world['viagens']['id']}/cargas",
                           json={"produto_id": world["produtos"]["id"], "produtor_id": world["produtor"],
                                 "identificacao": "C-2"})
    assert response.status_code == 422


def test_vehicle_requires_transportadora(client, world):
    assert client.post("/api/v1/veiculos", json={"empresa_id": world["produtor"],
                       "identificador": "V-2"}).status_code == 422


@pytest.fixture
def admin_headers(db, monkeypatch):
    from app.core.config import settings
    from app.core.security import create_access_token
    from app.models.usuario import Perfil, Usuario, EmpresaUsuario
    from scripts.setup_admin import setup_admin

    for model in (Perfil, Usuario, EmpresaUsuario):
        model.__table__.create(db.get_bind())
    monkeypatch.setattr(settings, "secret_key", "test-only-signing-key-never-use-in-production")
    admin, _ = setup_admin(db, "Admin teste", "admin@example.com", "test-only-password-123")
    return {"Authorization": f"Bearer {create_access_token(admin.id)}"}


@pytest.mark.parametrize("company_key,new_type", [
    ("transportadora", "CLIENTE"),
    ("transportadora", "PRODUTOR"),
    ("produtor", "TRANSPORTADORA"),
    ("produtor", "CLIENTE"),
    ("cliente", "TRANSPORTADORA"),
    ("cliente", "PRODUTOR"),
])
def test_company_type_change_preserves_logistics(client, world, db, admin_headers, company_key, new_type):
    company = db.get(Empresa, UUID(world[company_key]))
    original_type, original_name = company.tipo, company.nome
    response = client.patch(f"/api/v1/empresas/{company.id}", headers=admin_headers,
                            json={"tipo": new_type, "nome": "Nao deve ser aplicado"})
    assert response.status_code == 409
    assert "vinculos logisticos" in response.json()["detail"]
    db.refresh(company)
    assert company.tipo == original_type and company.nome == original_name
    assert client.get(f"/api/v1/viagens/{world['viagens']['id']}").status_code == 200
    assert client.get(f"/api/v1/cargas/{world['cargas']['id']}").status_code == 200
    assert client.get(f"/api/v1/caixas/{world['caixas']['id']}").status_code == 200
    assert client.patch(f"/api/v1/veiculos/{world['veiculos']['id']}", json={"ativo": False}).status_code == 200


@pytest.mark.parametrize("resource", ["veiculos", "motoristas"])
def test_company_type_change_with_only_one_inactive_link(client, db, admin_headers, resource):
    company = Empresa(nome="Transportadora teste", tipo=TipoEmpresa.TRANSPORTADORA, ativo=True)
    db.add(company)
    db.commit()
    data = {"empresa_id": str(company.id), "ativo": False}
    data.update({"identificador": "V-1"} if resource == "veiculos" else {"nome": "Motorista teste"})
    record = post(client, "/" + resource, data)
    response = client.patch(f"/api/v1/empresas/{company.id}", headers=admin_headers, json={"tipo": "CLIENTE"})
    assert response.status_code == 409
    assert client.get(f"/api/v1/{resource}/{record['id']}").json()["ativo"] is False


def test_company_same_type_update_allowed(client, world, admin_headers):
    response = client.patch(f"/api/v1/empresas/{world['transportadora']}", headers=admin_headers,
                            json={"tipo": "TRANSPORTADORA", "nome": "Nome atualizado"})
    assert response.status_code == 200
    assert response.json()["nome"] == "Nome atualizado"


def test_company_without_logistics_can_change_type(client, db, admin_headers):
    company = Empresa(nome="Sem vinculos", tipo=TipoEmpresa.TRANSPORTADORA, ativo=True)
    db.add(company)
    db.commit()
    response = client.patch(f"/api/v1/empresas/{company.id}", headers=admin_headers, json={"tipo": "CLIENTE"})
    assert response.status_code == 200
    assert response.json()["tipo"] == "CLIENTE"


def test_new_box_in_cancelled_trip_rejected_without_changing_children(client, world, db):
    from sqlalchemy import func

    assert client.patch(f"/api/v1/viagens/{world['viagens']['id']}", json={"status": "CANCELADA"}).status_code == 200
    count_before = db.scalar(select(func.count()).select_from(Caixa))
    response = client.post(f"/api/v1/cargas/{world['cargas']['id']}/caixas", json={"identificacao": "CX-2"})
    assert response.status_code == 422
    assert "viagem cancelada" in response.json()["detail"]
    assert db.scalar(select(func.count()).select_from(Caixa)) == count_before
    assert client.get(f"/api/v1/cargas/{world['cargas']['id']}").json()["status"] == "PLANEJADA"
    assert client.get(f"/api/v1/caixas/{world['caixas']['id']}").json()["status"] == "REGISTRADA"
    assert client.patch(f"/api/v1/caixas/{world['caixas']['id']}",
                        json={"observacoes": "Preservacao do historico"}).status_code == 200


@pytest.mark.parametrize("schema_name", ["CargaCreate", "CargaUpdate"])
@pytest.mark.parametrize("value,accepted", [
    (0, True),
    (2147483647, True),
    (2147483648, False),
    (-1, False),
])
def test_quantity_boxes_schema_boundaries(schema_name, value, accepted):
    from pydantic import ValidationError
    from app.modules.logistica import schemas

    schema = getattr(schemas, schema_name)
    data = {"quantidade_caixas": value}
    if schema_name == "CargaCreate":
        data.update({"produto_id": uuid4(), "produtor_id": uuid4(), "identificacao": "C-1"})
    if accepted:
        assert schema.model_validate(data).quantidade_caixas == value
    else:
        with pytest.raises(ValidationError):
            schema.model_validate(data)


@pytest.mark.parametrize("operation", ["create", "update"])
def test_quantity_boxes_overflow_rejected_before_service(client, world, monkeypatch, operation):
    from app.modules.logistica.service import CargaService

    def must_not_run(*args, **kwargs):
        pytest.fail("Quantidade invalida deve ser rejeitada antes do service/banco.")

    monkeypatch.setattr(CargaService, operation, must_not_run)
    if operation == "create":
        response = client.post(f"/api/v1/viagens/{world['viagens']['id']}/cargas",
                               json={"produto_id": world["produtos"]["id"], "produtor_id": world["produtor"],
                                     "identificacao": "C-2", "quantidade_caixas": 2147483648})
    else:
        response = client.patch(f"/api/v1/cargas/{world['cargas']['id']}", json={"quantidade_caixas": 2147483648})
    assert response.status_code == 422
    assert any(error["loc"][-1] == "quantidade_caixas" for error in response.json()["detail"])
