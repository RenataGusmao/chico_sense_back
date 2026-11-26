import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4

import httpx
import jwt
import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_database_session
from app.core.config import settings
from app.core.security import create_access_token
from app.main import create_app
from app.modules.integracoes.thingspeak.client import ThingSpeakClient
from app.modules.inteligencia import service
from app.modules.inteligencia.thingspeak_service import ThingSpeakService
from app.repositories.usuarios import UsuarioRepository


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(settings, "secret_key", "test-only-signing-key-never-use-in-production")
    users = {
        role: SimpleNamespace(id=uuid4(), ativo=True, perfil=SimpleNamespace(nome=role))
        for role in ("ADMIN", "CONSULTA")
    }
    monkeypatch.setattr(UsuarioRepository, "get", lambda self, id: next(
        (user for user in users.values() if user.id == id), None
    ))
    app = create_app()
    app.dependency_overrides[get_database_session] = lambda: None
    with TestClient(app) as api:
        yield api, {
            role: {"Authorization": f"Bearer {create_access_token(user.id)}"}
            for role, user in users.items()
        }


def medicoes(temperaturas=None, fim=None):
    temperaturas = temperaturas or [13, 13.1, 13.2, 13.1, 13.2]
    fim = fim or datetime(2026, 11, 26, 15, 1, 20, tzinfo=timezone.utc)
    return [
        {
            "data_hora": (fim - timedelta(seconds=20 * (len(temperaturas) - 1 - i))).isoformat(),
            "temperatura": temp,
            "umidade": 85.0,
        }
        for i, temp in enumerate(temperaturas)
    ]


def analisar(client, dados):
    api, headers = client
    return api.post("/api/v1/ia/analisar", headers=headers["CONSULTA"], json={"medicoes": dados})


@pytest.mark.parametrize("method,path,admin", [
    ("GET", "/status", False), ("GET", "/historico", True),
    ("POST", "/analisar", False), ("GET", "/thingspeak", True),
])
def test_permissoes(client, method, path, admin):
    api, headers = client
    url = "/api/v1/ia" + path
    payload = {"json": {"medicoes": []}} if method == "POST" else {}
    expired_payload = jwt.decode(headers["ADMIN"]["Authorization"].split()[1], options={"verify_signature": False})
    expired_payload["exp"] = datetime.now(timezone.utc) - timedelta(seconds=60)
    expired = jwt.encode(expired_payload, settings.secret_key, algorithm="HS256")
    for credentials in ({}, {"Authorization": "Bearer invalid"}, {"Authorization": f"Bearer {expired}"}):
        assert api.request(method, url, headers=credentials, **payload).status_code == 401
    response = api.request(method, url, headers=headers["CONSULTA"], **payload)
    assert response.status_code == (403 if admin else 200)


def test_artefatos_e_inferencia(client):
    api, headers = client
    status = api.get("/api/v1/ia/status", headers=headers["CONSULTA"]).json()
    assert status["disponivel"] and status["features"] == service.FEATURES
    assert status["modo"] == "EXPERIMENTAL"
    historico = api.get("/api/v1/ia/historico", headers=headers["ADMIN"])
    assert historico.status_code == 200
    assert historico.json()["monitoramento_tempo_real"] is False
    assert historico.json()["resultado"]["total_avaliado"] == 466

    resultados = []
    for serie in (medicoes(), medicoes([13, 13.1, 13.2, 13.1, 49])):
        response = analisar(client, serie)
        assert response.status_code == 200
        dados = response.json()
        assert dados["anomalia"] == (dados["score"] > dados["limite"])
        assert set(dados["fatores_considerados"]) == set(service.FEATURES)
        assert dados["status"] == ("ANOMALIA_DETECTADA" if dados["anomalia"] else "NAO_SINALIZADO")
        resultados.append(dados)
    assert resultados[0]["score"] != resultados[1]["score"]
    assert analisar(client, list(reversed(medicoes()))).json() == resultados[0]


@pytest.mark.parametrize("caso", ["ausente", "corrompido", "metadados", "pacote"])
def test_modelo_indisponivel(client, monkeypatch, tmp_path, caso):
    api, headers = client
    service.carregar_modelo.cache_clear()
    if caso in {"ausente", "corrompido"}:
        caminho = tmp_path / "modelo.joblib"
        if caso == "corrompido":
            caminho.write_bytes(b"")
        monkeypatch.setattr(service, "ARQUIVO_MODELO", caminho)
    elif caso == "metadados":
        caminho = tmp_path / "metadados.json"
        caminho.write_text(json.dumps({**service.obter_metadados(), "features": []}), encoding="utf-8")
        monkeypatch.setattr(service, "ARQUIVO_METADADOS", caminho)
    else:
        monkeypatch.setattr(service.joblib, "load", lambda path: {"features": []})
    assert api.get("/api/v1/ia/status", headers=headers["ADMIN"]).json()["disponivel"] is False
    assert analisar(client, medicoes()).status_code == 503


@pytest.mark.parametrize("conteudo", [None, "{", "[]", '{"score": 1e999}'])
def test_historico_indisponivel(client, monkeypatch, tmp_path, conteudo):
    api, headers = client
    monkeypatch.setattr(service, "PASTA_RESULTADOS", tmp_path)
    if conteudo is not None:
        (tmp_path / "resumo_avaliacao.json").write_text(conteudo, encoding="utf-8")
    assert api.get("/api/v1/ia/historico", headers=headers["ADMIN"]).status_code == 503


@pytest.mark.parametrize("campo,valor", [
    ("temperatura", -274), ("temperatura", 1e99), ("umidade", -1), ("umidade", 101),
])
def test_dados_invalidos(client, campo, valor):
    dados = medicoes()
    dados[-1][campo] = valor
    response = analisar(client, dados)
    assert response.status_code == 200
    assert response.json()["status"] == "DADOS_INVALIDOS"


def test_duplicadas_e_interrupcao(client):
    dados = medicoes()
    dados[-1]["data_hora"] = dados[-2]["data_hora"]
    assert analisar(client, dados).json()["status"] == "DADOS_INVALIDOS"
    dados[-1]["data_hora"] = "2026-11-26T15:02:01Z"
    assert analisar(client, dados).json()["status"] == "DADOS_INSUFICIENTES"
    assert analisar(client, []).json()["status"] == "DADOS_INSUFICIENTES"
    assert analisar(client, medicoes()[:4]).json()["status"] == "DADOS_INSUFICIENTES"


@pytest.mark.parametrize("payload", [
    {}, {"medicoes": "errado"}, {"medicoes": [{"temperatura": 13}]},
    {"medicoes": [{"data_hora": "errado", "temperatura": 13, "umidade": 80}]},
    {"medicoes": [{"data_hora": "2026-11-26T15:00:00Z", "temperatura": "NaN", "umidade": 80}]},
    {"medicoes": [{"data_hora": "2026-11-26T15:00:00Z", "temperatura": 13, "umidade": "inf"}]},
])
def test_schema(client, payload):
    api, headers = client
    response = api.post("/api/v1/ia/analisar", json=payload, headers=headers["ADMIN"])
    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)


def test_limite_medicoes(client):
    assert analisar(client, medicoes([13] * 1000)).status_code == 200
    assert analisar(client, medicoes([13] * 1001)).status_code == 422


@pytest.mark.parametrize("caso,http,status", [
    ("sem_canal", 200, "CANAL_NAO_CONFIGURADO"),
    ("canal_vazio", 200, "CANAL_NAO_CONFIGURADO"),
    ("vazio", 200, "DADOS_INSUFICIENTES"),
    ("medicao_invalida", 200, "DADOS_INSUFICIENTES"),
    ("antigo", 200, "DADOS_DESATUALIZADOS"),
    ("futuro", 200, "HORARIO_INVALIDO"),
    ("duplicado", 200, "DADOS_INVALIDOS"),
    ("interrupcao", 200, "INTERRUPCAO_DETECTADA"),
    ("valido", 200, None),
    ("modelo_ausente", 503, None),
    ("timeout", 504, None),
    ("conexao", 503, None),
    ("configuracao_invalida", 503, None),
    ("erro_http", 502, None),
    ("sem_feeds", 502, None),
    ("formato_errado", 502, None),
    ("item_errado", 502, None),
])
def test_thingspeak(client, monkeypatch, tmp_path, caso, http, status):
    api, headers = client
    canal = {
        "sem_canal": None, "canal_vazio": "",
        "configuracao_invalida": "invalido/segredo-ficticio",
    }.get(caso, "3493148")
    monkeypatch.setattr(settings, "thingspeak_channel_id", canal)
    fim = datetime.now(timezone.utc) - timedelta(seconds=4)
    if caso == "antigo":
        fim -= timedelta(seconds=120)
    elif caso == "futuro":
        fim += timedelta(seconds=60)
    feeds = [
        {"entry_id": i, "created_at": d["data_hora"], "field1": str(d["temperatura"]), "field2": str(d["umidade"])}
        for i, d in enumerate(medicoes(fim=fim))
    ]
    if caso == "vazio":
        feeds = []
    elif caso == "medicao_invalida":
        feeds[0]["field2"] = "NaN"
    elif caso == "duplicado":
        feeds[1]["created_at"] = feeds[0]["created_at"]
    elif caso == "interrupcao":
        feeds[0]["created_at"] = (fim - timedelta(seconds=122)).isoformat()
    elif caso == "modelo_ausente":
        service.carregar_modelo.cache_clear()
        monkeypatch.setattr(service, "ARQUIVO_MODELO", tmp_path / "ausente.joblib")

    def mock(request):
        assert caso != "configuracao_invalida"
        assert request.method == "GET"
        assert request.url.params["results"] == "5"
        if caso == "timeout":
            raise httpx.ReadTimeout("timeout", request=request)
        if caso == "conexao":
            raise httpx.ConnectError("connection", request=request)
        if caso == "erro_http":
            return httpx.Response(503)
        payload = {"feeds": list(reversed(feeds))}
        if caso == "sem_feeds":
            payload = {}
        elif caso == "formato_errado":
            payload = {"feeds": {}}
        elif caso == "item_errado":
            payload = {"feeds": [123]}
        return httpx.Response(200, json=payload)

    servico = ThingSpeakService.from_settings()
    servico.client = ThingSpeakClient(
        base_url="https://api.thingspeak.com",
        http_client=httpx.AsyncClient(base_url="https://api.thingspeak.com", transport=httpx.MockTransport(mock)),
    )
    monkeypatch.setattr(ThingSpeakService, "from_settings", lambda: servico)
    response = api.get("/api/v1/ia/thingspeak", headers=headers["ADMIN"])
    assert response.status_code == http
    assert "segredo-ficticio" not in response.text
    if status:
        assert response.json()["status"] == status
        assert response.json()["resultado"] is None
    elif caso == "valido":
        dados = response.json()
        assert dados["dados_recentes"] and len(dados["medicoes"]) == 5
        assert dados["status"] == dados["resultado"]["status"]
        assert dados["resultado"]["origem"] == "THINGSPEAK"
