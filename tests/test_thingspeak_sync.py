from __future__ import annotations

import asyncio
import uuid
from contextlib import nullcontext

from fastapi.testclient import TestClient

from app.main import app
from app.modules.integracoes.thingspeak import routes as thingspeak_routes
from app.modules.integracoes.thingspeak.client import ThingSpeakClient
from app.modules.integracoes.thingspeak.mapper import ThingSpeakFieldMapper
from app.modules.integracoes.thingspeak.schemas import (
    ThingSpeakChannelConfig,
    ThingSpeakFieldMapping,
    ThingSpeakMappingConfig,
    ThingSpeakSyncSummary,
)
from app.modules.integracoes.thingspeak.service import ThingSpeakService
from tests.test_thingspeak_integration import MockAsyncClient, make_response


class FakeDispositivo:
    def __init__(self, viagem_id: uuid.UUID | None, carga_id: uuid.UUID | None) -> None:
        self.viagem_id = viagem_id
        self.carga_id = carga_id


class FakeSensor:
    def __init__(self, sensor_id: uuid.UUID, viagem_id: uuid.UUID | None, carga_id: uuid.UUID | None) -> None:
        self.id = sensor_id
        self.dispositivo = FakeDispositivo(viagem_id=viagem_id, carga_id=carga_id)


class FakeDB:
    def __init__(self) -> None:
        self.commits = 0

    def begin_nested(self):
        return nullcontext()

    def commit(self) -> None:
        self.commits += 1


class FakeSensorRepository:
    sensors: dict[uuid.UUID, FakeSensor] = {}

    def __init__(self, db: FakeDB) -> None:
        self.db = db

    def get_with_dispositivo(self, sensor_id: uuid.UUID) -> FakeSensor | None:
        return self.sensors.get(sensor_id)


class FakeMedicao:
    def __init__(self, medicao_id: uuid.UUID) -> None:
        self.id = medicao_id


class FakeMedicaoRepository:
    created: list[dict] = []
    fail_for_fields: set[str] = set()

    def __init__(self, db: FakeDB) -> None:
        self.db = db

    def create(self, **kwargs) -> FakeMedicao:
        if kwargs.get("unidade") in self.fail_for_fields:
            raise RuntimeError("forced failure")
        self.created.append(kwargs)
        return FakeMedicao(uuid.uuid4())


class FakeLeituraExternaRepository:
    existing_keys: set[tuple[str, str, int, str]] = set()
    created: list[dict] = []

    def __init__(self, db: FakeDB) -> None:
        self.db = db

    def exists(self, *, origem: str, channel_id: str, entry_id: int, field_name: str) -> bool:
        return (origem, channel_id, entry_id, field_name) in self.existing_keys

    def create(self, **kwargs):
        key = (kwargs["origem"], kwargs["channel_id"], kwargs["entry_id"], kwargs["field_name"])
        self.existing_keys.add(key)
        self.created.append(kwargs)
        return object()


def reset_fakes() -> None:
    FakeSensorRepository.sensors = {}
    FakeMedicaoRepository.created = []
    FakeMedicaoRepository.fail_for_fields = set()
    FakeLeituraExternaRepository.existing_keys = set()
    FakeLeituraExternaRepository.created = []


def build_service(payload: dict, mapping: dict[str, ThingSpeakFieldMapping]) -> ThingSpeakService:
    client = ThingSpeakClient(
        "https://api.thingspeak.com",
        read_api_key="SECRET_READ_KEY",
        http_client=MockAsyncClient(make_response(200, payload)),
    )
    mapper = ThingSpeakFieldMapper(ThingSpeakMappingConfig(fields=mapping))
    return ThingSpeakService(
        config=ThingSpeakChannelConfig(
            base_url="https://api.thingspeak.com",
            channel_id="123",
            read_api_key="SECRET_READ_KEY",
        ),
        client=client,
        mapper=mapper,
    )


def patch_repositories(monkeypatch) -> None:
    monkeypatch.setattr("app.modules.integracoes.thingspeak.service.SensorRepository", FakeSensorRepository)
    monkeypatch.setattr("app.modules.integracoes.thingspeak.service.MedicaoRepository", FakeMedicaoRepository)
    monkeypatch.setattr(
        "app.modules.integracoes.thingspeak.service.LeituraExternaRepository",
        FakeLeituraExternaRepository,
    )


def test_sync_valid_feed_creates_medicao_and_external_tracking(monkeypatch) -> None:
    reset_fakes()
    patch_repositories(monkeypatch)
    sensor_id = uuid.uuid4()
    viagem_id = uuid.uuid4()
    carga_id = uuid.uuid4()
    FakeSensorRepository.sensors[sensor_id] = FakeSensor(sensor_id, viagem_id, carga_id)
    service = build_service(
        {
            "channel": {"id": 123},
            "feeds": [{"created_at": "2026-10-02T12:00:00Z", "entry_id": 1, "field1": "25.3"}],
        },
        {"field1": ThingSpeakFieldMapping(sensor_id=sensor_id, contexto="AMBIENTE", unidade="C")},
    )

    summary = asyncio.run(service.sincronizar_feeds(FakeDB(), results=1))

    assert summary.feeds_recebidos == 1
    assert summary.fields_processados == 1
    assert summary.medicoes_criadas == 1
    assert FakeMedicaoRepository.created[0]["sensor_id"] == sensor_id
    assert FakeLeituraExternaRepository.created[0]["entry_id"] == 1
    assert FakeLeituraExternaRepository.created[0]["field_name"] == "field1"


def test_sync_same_reading_twice_does_not_duplicate(monkeypatch) -> None:
    reset_fakes()
    patch_repositories(monkeypatch)
    sensor_id = uuid.uuid4()
    FakeSensorRepository.sensors[sensor_id] = FakeSensor(sensor_id, uuid.uuid4(), uuid.uuid4())
    service = build_service(
        {
            "channel": {"id": 123},
            "feeds": [{"created_at": "2026-10-02T12:00:00Z", "entry_id": 1, "field1": "25.3"}],
        },
        {"field1": ThingSpeakFieldMapping(sensor_id=sensor_id, contexto="AMBIENTE", unidade="C")},
    )

    first = asyncio.run(service.sincronizar_feeds(FakeDB(), results=1))
    second = asyncio.run(service.sincronizar_feeds(FakeDB(), results=1))

    assert first.medicoes_criadas == 1
    assert second.medicoes_criadas == 0
    assert second.duplicados == 1


def test_sync_ignores_null_empty_and_non_numeric_values(monkeypatch) -> None:
    reset_fakes()
    patch_repositories(monkeypatch)
    sensor_id = uuid.uuid4()
    FakeSensorRepository.sensors[sensor_id] = FakeSensor(sensor_id, uuid.uuid4(), uuid.uuid4())
    service = build_service(
        {
            "channel": {"id": 123},
            "feeds": [
                {
                    "created_at": "2026-10-02T12:00:00Z",
                    "entry_id": 1,
                    "field1": None,
                    "field2": "",
                    "field3": "abc",
                }
            ],
        },
        {
            "field1": ThingSpeakFieldMapping(sensor_id=sensor_id, contexto="AMBIENTE", unidade="C"),
            "field2": ThingSpeakFieldMapping(sensor_id=sensor_id, contexto="AMBIENTE", unidade="C"),
            "field3": ThingSpeakFieldMapping(sensor_id=sensor_id, contexto="AMBIENTE", unidade="C"),
        },
    )

    summary = asyncio.run(service.sincronizar_feeds(FakeDB(), results=1))

    assert summary.medicoes_criadas == 0
    assert summary.ignorados == 3
    assert {error.motivo for error in summary.erros} == {"empty_value", "invalid_numeric_value"}


def test_sync_ignores_missing_sensor_and_unconfigured_field(monkeypatch) -> None:
    reset_fakes()
    patch_repositories(monkeypatch)
    missing_sensor_id = uuid.uuid4()
    service = build_service(
        {
            "channel": {"id": 123},
            "feeds": [{"created_at": "2026-10-02T12:00:00Z", "entry_id": 1, "field1": "25.3", "field2": "70"}],
        },
        {"field1": ThingSpeakFieldMapping(sensor_id=missing_sensor_id, contexto="AMBIENTE", unidade="C")},
    )

    summary = asyncio.run(service.sincronizar_feeds(FakeDB(), results=1))

    assert summary.fields_processados == 1
    assert summary.ignorados == 1
    assert summary.erros[0].motivo == "sensor_not_found"


def test_sync_multiple_fields_partial_error_keeps_valid_records(monkeypatch) -> None:
    reset_fakes()
    patch_repositories(monkeypatch)
    sensor_id = uuid.uuid4()
    FakeSensorRepository.sensors[sensor_id] = FakeSensor(sensor_id, uuid.uuid4(), uuid.uuid4())
    FakeMedicaoRepository.fail_for_fields = {"FAIL"}
    service = build_service(
        {
            "channel": {"id": 123},
            "feeds": [{"created_at": "2026-10-02T12:00:00Z", "entry_id": 1, "field1": "25.3", "field2": "70"}],
        },
        {
            "field1": ThingSpeakFieldMapping(sensor_id=sensor_id, contexto="AMBIENTE", unidade="C"),
            "field2": ThingSpeakFieldMapping(sensor_id=sensor_id, contexto="AMBIENTE", unidade="FAIL"),
        },
    )

    summary = asyncio.run(service.sincronizar_feeds(FakeDB(), results=1))

    assert summary.medicoes_criadas == 1
    assert summary.ignorados == 1
    assert summary.erros[0].motivo == "persistence_error"


def test_sync_endpoint_returns_summary_and_does_not_expose_api_key(monkeypatch) -> None:
    async def fake_sync(self, db, results=None):
        return ThingSpeakSyncSummary(
            feeds_recebidos=1,
            fields_processados=1,
            medicoes_criadas=1,
            duplicados=0,
            ignorados=0,
            erros=[],
        )

    def fake_db():
        yield FakeDB()

    monkeypatch.setattr(thingspeak_routes.ThingSpeakService, "sincronizar_feeds", fake_sync)
    app.dependency_overrides[thingspeak_routes.get_database_session] = fake_db

    response = TestClient(app).post("/api/v1/integracoes/thingspeak/sincronizar?results=1")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    payload = response.json()
    assert payload["medicoes_criadas"] == 1
    assert "SECRET_READ_KEY" not in response.text

