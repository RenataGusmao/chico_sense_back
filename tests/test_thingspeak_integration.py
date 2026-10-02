from __future__ import annotations

import asyncio
from decimal import Decimal

import httpx
import pytest

from app.modules.integracoes.thingspeak.client import ThingSpeakClient
from app.modules.integracoes.thingspeak.exceptions import (
    ThingSpeakConfigurationError,
    ThingSpeakHTTPError,
    ThingSpeakInvalidResponseError,
    ThingSpeakTimeoutError,
)
from app.modules.integracoes.thingspeak.mapper import ThingSpeakFieldMapper
from app.modules.integracoes.thingspeak.schemas import (
    ThingSpeakChannelConfig,
    ThingSpeakFeed,
    ThingSpeakFieldMapping,
    ThingSpeakMappingConfig,
)
from app.modules.integracoes.thingspeak.service import ThingSpeakService


class MockAsyncClient:
    def __init__(self, response: httpx.Response | None = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.last_path: str | None = None
        self.last_params: dict | None = None

    async def get(self, path: str, params: dict | None = None) -> httpx.Response:
        self.last_path = path
        self.last_params = params
        if self.error:
            raise self.error
        assert self.response is not None
        return self.response


def make_response(status_code: int, payload: dict | None = None, content: bytes | None = None) -> httpx.Response:
    request = httpx.Request("GET", "https://api.thingspeak.com/test")
    if content is not None:
        return httpx.Response(status_code=status_code, content=content, request=request)
    return httpx.Response(status_code=status_code, json=payload, request=request)


def test_valid_feed_reading_is_parsed() -> None:
    mock_client = MockAsyncClient(
        make_response(
            200,
            {
                "channel": {"id": 123, "name": "Canal ChicoSense"},
                "feeds": [{"created_at": "2026-10-02T12:00:00Z", "entry_id": 7, "field1": "25.3"}],
            },
        )
    )
    client = ThingSpeakClient("https://api.thingspeak.com", http_client=mock_client)

    response = asyncio.run(client.get_feeds("123", results=1))

    assert len(response.feeds) == 1
    assert response.feeds[0].entry_id == 7
    assert response.feeds[0].fields["field1"] == "25.3"


def test_channel_with_empty_feeds_returns_empty_list() -> None:
    mock_client = MockAsyncClient(make_response(200, {"channel": {"id": 123}, "feeds": []}))
    client = ThingSpeakClient("https://api.thingspeak.com", http_client=mock_client)

    response = asyncio.run(client.get_feeds("123"))

    assert response.feeds == []


def test_mapper_handles_null_field_without_failing() -> None:
    feed = ThingSpeakFeed.from_api_payload(
        {"created_at": "2026-10-02T12:00:00Z", "entry_id": 1, "field1": None}
    )
    mapper = ThingSpeakFieldMapper(
        ThingSpeakMappingConfig(
            fields={"field1": ThingSpeakFieldMapping(tipo="TEMPERATURA", contexto="AMBIENTE", unidade="C")}
        )
    )

    readings = mapper.map_feed("123", feed)

    assert len(readings) == 1
    assert readings[0].valor is None
    assert readings[0].ignorada is True
    assert readings[0].motivo_ignorada == "empty_value"


def test_timeout_is_mapped_to_domain_exception() -> None:
    mock_client = MockAsyncClient(error=httpx.TimeoutException("timeout"))
    client = ThingSpeakClient("https://api.thingspeak.com", http_client=mock_client)

    with pytest.raises(ThingSpeakTimeoutError):
        asyncio.run(client.get_feeds("123"))


def test_http_404_is_mapped_to_domain_exception() -> None:
    mock_client = MockAsyncClient(make_response(404, {"error": "not found"}))
    client = ThingSpeakClient("https://api.thingspeak.com", http_client=mock_client)

    with pytest.raises(ThingSpeakHTTPError) as exc:
        asyncio.run(client.get_feeds("123"))

    assert exc.value.status_code == 404


def test_invalid_json_response_is_rejected() -> None:
    mock_client = MockAsyncClient(make_response(200, content=b"not-json"))
    client = ThingSpeakClient("https://api.thingspeak.com", http_client=mock_client)

    with pytest.raises(ThingSpeakInvalidResponseError):
        asyncio.run(client.get_feeds("123"))


def test_configurable_field_mapping_converts_values() -> None:
    feed = ThingSpeakFeed.from_api_payload(
        {"created_at": "2026-10-02T12:00:00Z", "entry_id": 10, "field1": "25.3", "field2": "70.1"}
    )
    mapper = ThingSpeakFieldMapper(
        ThingSpeakMappingConfig(
            fields={
                "field1": ThingSpeakFieldMapping(tipo="TEMPERATURA", contexto="AMBIENTE", unidade="C"),
                "field2": ThingSpeakFieldMapping(tipo="UMIDADE", contexto="AMBIENTE", unidade="%"),
            }
        )
    )

    readings = mapper.map_feed("123", feed)

    assert [reading.field_name for reading in readings] == ["field1", "field2"]
    assert readings[0].valor == Decimal("25.3")
    assert readings[1].valor == Decimal("70.1")


def test_missing_channel_id_does_not_crash_status_and_blocks_queries() -> None:
    service = ThingSpeakService(
        config=ThingSpeakChannelConfig(base_url="https://api.thingspeak.com"),
        client=ThingSpeakClient("https://api.thingspeak.com", http_client=MockAsyncClient()),
        mapper=ThingSpeakFieldMapper(ThingSpeakMappingConfig()),
    )

    status = service.get_status()

    assert status.configured is False
    assert "not configured" in status.message
    with pytest.raises(ThingSpeakConfigurationError):
        asyncio.run(service.get_feeds())


def test_api_key_is_not_exposed_in_status_response_or_logs(caplog: pytest.LogCaptureFixture) -> None:
    secret = "SECRET_READ_KEY"
    mock_client = MockAsyncClient(make_response(200, {"channel": {"id": 123}, "feeds": []}))
    client = ThingSpeakClient("https://api.thingspeak.com", read_api_key=secret, http_client=mock_client)
    service = ThingSpeakService(
        config=ThingSpeakChannelConfig(
            base_url="https://api.thingspeak.com",
            channel_id="123",
            read_api_key=secret,
        ),
        client=client,
        mapper=ThingSpeakFieldMapper(ThingSpeakMappingConfig()),
    )

    status_payload = service.get_status().model_dump()
    asyncio.run(service.get_feeds())

    assert secret not in str(status_payload)
    assert secret not in caplog.text
    assert mock_client.last_params["api_key"] == secret


def test_external_deduplication_key_is_preserved_for_future_persistence() -> None:
    feed = ThingSpeakFeed.from_api_payload(
        {"created_at": "2026-10-02T12:00:00Z", "entry_id": 99, "field1": "25.3"}
    )
    mapper = ThingSpeakFieldMapper(
        ThingSpeakMappingConfig(fields={"field1": ThingSpeakFieldMapping(tipo="TEMPERATURA")})
    )

    reading = mapper.map_feed("123", feed)[0]

    assert (reading.channel_id, reading.entry_id, reading.field_name) == ("123", 99, "field1")

