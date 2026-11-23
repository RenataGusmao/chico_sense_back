"""Explicit browser origin policy; no external network or application database."""
import json
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from app.api.deps import get_database_session
from app.core.config import Settings, settings
from app.main import LOCAL_FRONTEND_ORIGINS, create_app

PRODUCTION = "https://chico-sense-frontend.vercel.app"
PREVIEW = "https://chico-sense-frontend-q5lqczbcw-juuvalentin95-1633s-projects.vercel.app"


@pytest.fixture
def cors_client(monkeypatch):
    monkeypatch.setattr(settings, "cors_allowed_origins", [PRODUCTION, PREVIEW])
    application = create_app()
    # A malformed login must be rejected by validation, without opening a DB.
    application.dependency_overrides[get_database_session] = lambda: None
    with TestClient(application) as client:
        yield client


@pytest.mark.parametrize("origin", [PRODUCTION, PREVIEW, *LOCAL_FRONTEND_ORIGINS])
def test_allowed_origins_preflight_and_health(cors_client, origin):
    response = cors_client.options("/api/v1/auth/login", headers={
        "Origin": origin,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type,authorization",
    })
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
    assert response.headers["access-control-allow-credentials"] == "true"
    assert {"GET", "POST", "OPTIONS"} <= set(response.headers["access-control-allow-methods"].split(", "))
    assert response.headers["access-control-allow-headers"] == "content-type,authorization"
    assert "Origin" in response.headers["vary"]
    health = cors_client.get("/health", headers={"Origin": origin})
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert health.headers["access-control-allow-origin"] == origin


@pytest.mark.parametrize("origin", ["https://untrusted.example", "https://other-preview.vercel.app", PRODUCTION + ".evil.example"])
def test_unknown_origins_are_not_allowed(cors_client, origin):
    headers = {"Origin": origin, "Access-Control-Request-Method": "POST"}
    response = cors_client.options("/api/v1/auth/login", headers=headers)
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers
    response = cors_client.get("/health", headers={"Origin": origin})
    assert response.status_code == 200  # CORS is a browser policy, not server authentication.
    assert "access-control-allow-origin" not in response.headers


def test_validation_and_private_routes_keep_their_protection(cors_client):
    response = cors_client.post("/api/v1/auth/login", json={}, headers={"Origin": PRODUCTION})
    assert response.status_code == 422
    assert response.headers["access-control-allow-origin"] == PRODUCTION
    assert {error["loc"][-1] for error in response.json()["detail"]} == {"email", "senha"}
    response = cors_client.get("/api/v1/auth/me", headers={"Origin": PRODUCTION})
    assert response.status_code == 401
    assert response.headers["access-control-allow-origin"] == PRODUCTION


def test_environment_json_list_is_loaded_and_normalized(monkeypatch):
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", '["' + PRODUCTION + '/", "' + PREVIEW + '", "' + PRODUCTION + '"]')
    config = Settings(_env_file=None)
    assert config.cors_allowed_origins == [PRODUCTION, PREVIEW]


def test_default_keeps_local_origins_only(monkeypatch):
    monkeypatch.delenv("CORS_ALLOWED_ORIGINS", raising=False)
    config = Settings(_env_file=None)
    assert config.cors_allowed_origins == []
    monkeypatch.setattr(settings, "cors_allowed_origins", config.cors_allowed_origins)
    with TestClient(create_app()) as client:
        for origin in LOCAL_FRONTEND_ORIGINS:
            assert client.get("/health", headers={"Origin": origin}).headers["access-control-allow-origin"] == origin
        assert "access-control-allow-origin" not in client.get("/health", headers={"Origin": PRODUCTION}).headers


@pytest.mark.parametrize("origin", ["*", "https://*.vercel.app", "https://example.com/path", "https://user:pass@example.com", "https://example.com?x=1", "https://example.com#fragment", "ftp://example.com", "not-a-url", "https://example.com:bad", "https://example.com:0"])
def test_invalid_origin_configuration_is_rejected(origin, monkeypatch):
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", json.dumps([origin]))
    with pytest.raises(ValidationError):
        Settings(_env_file=None)
