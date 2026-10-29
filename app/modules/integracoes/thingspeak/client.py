from __future__ import annotations

import logging
from typing import Any

import httpx
from pydantic import ValidationError

from app.modules.integracoes.thingspeak.exceptions import (
    ThingSpeakConnectionError,
    ThingSpeakHTTPError,
    ThingSpeakInvalidResponseError,
    ThingSpeakTimeoutError,
)
from app.modules.integracoes.thingspeak.schemas import (
    ThingSpeakChannelMetadata,
    ThingSpeakFeed,
    ThingSpeakFeedsResponse,
)

logger = logging.getLogger(__name__)


class _ThingSpeakRequestLogFilter(logging.Filter):
    """HTTPX logs full query strings at INFO; sanitize keys during every ThingSpeak request."""
    def filter(self, record: logging.LogRecord) -> bool:
        import re
        message = re.sub(r"(?i)(https?://)[^/\s@]+@", r"\1[REDACTED]@", record.getMessage())
        record.msg = re.sub(r"(?i)([?&](?:api[_-]?key|read_api_key|write_api_key|token|access_token|password|secret)=)[^&\s\"]+",
                            r"\1[REDACTED]", message)
        record.args = ()
        return True


class ThingSpeakClient:
    def __init__(
        self,
        base_url: str,
        read_api_key: str | None = None,
        timeout_seconds: float = 10,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.read_api_key = read_api_key
        self.timeout = httpx.Timeout(timeout_seconds)
        self._http_client = http_client

    async def get_channel_info(self, channel_id: str) -> ThingSpeakChannelMetadata:
        payload = await self._get_json(f"/channels/{channel_id}.json")
        channel_payload = payload.get("channel", payload)
        try:
            return ThingSpeakChannelMetadata.model_validate(channel_payload)
        except ValidationError as exc:
            raise ThingSpeakInvalidResponseError("Invalid ThingSpeak channel response.") from exc

    async def get_feeds(self, channel_id: str, results: int | None = None) -> ThingSpeakFeedsResponse:
        params: dict[str, Any] = {}
        if results is not None:
            params["results"] = results

        payload = await self._get_json(f"/channels/{channel_id}/feeds.json", params=params)
        try:
            feeds = [ThingSpeakFeed.from_api_payload(feed) for feed in payload.get("feeds", [])]
            channel = payload.get("channel")
            return ThingSpeakFeedsResponse(
                channel=ThingSpeakChannelMetadata.model_validate(channel) if channel else None,
                feeds=feeds,
            )
        except (KeyError, TypeError, ValidationError) as exc:
            raise ThingSpeakInvalidResponseError("Invalid ThingSpeak feeds response.") from exc

    async def get_feeds_historicos(self, channel_id: str, inicio, fim, results: int = 8000) -> dict[str, Any]:
        """Raw window response for per-reading validation; reuse the existing HTTP client.

        No averaging, rounding or imputation is requested. Exact microsecond boundaries
        are enforced by the session consumer after the second-resolution query.
        """
        from datetime import timedelta, timezone
        inicio = inicio.astimezone(timezone.utc).replace(microsecond=0)
        fim = fim.astimezone(timezone.utc)
        if fim.microsecond:
            fim = fim.replace(microsecond=0) + timedelta(seconds=1)
        payload = await self._get_json(f"/channels/{channel_id}/feeds.json", params={
            "start": inicio.strftime("%Y-%m-%d %H:%M:%S"),
            "end": fim.strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": "UTC", "results": results,
        })
        if not isinstance(payload.get("feeds"), list):
            raise ThingSpeakInvalidResponseError("Invalid ThingSpeak historical feeds response.")
        channel = payload.get("channel")
        if channel is not None and (not isinstance(channel, dict) or str(channel.get("id")) != channel_id):
            raise ThingSpeakInvalidResponseError("Unexpected ThingSpeak historical channel.")
        return payload

    async def get_latest_feed(self, channel_id: str) -> ThingSpeakFeed | None:
        payload = await self._get_json(f"/channels/{channel_id}/feeds/last.json")
        if not payload:
            return None
        try:
            return ThingSpeakFeed.from_api_payload(payload)
        except (KeyError, TypeError, ValidationError) as exc:
            raise ThingSpeakInvalidResponseError("Invalid ThingSpeak latest feed response.") from exc

    async def _get_json(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        request_params = dict(params or {})
        if self.read_api_key:
            request_params["api_key"] = self.read_api_key

        safe_params = {key: value for key, value in request_params.items() if key != "api_key"}
        logger.info("Querying ThingSpeak path=%s params=%s", path, safe_params)

        request_logger = logging.getLogger("httpx")
        safe_filter = _ThingSpeakRequestLogFilter()
        request_logger.addFilter(safe_filter)
        try:
            if self._http_client is not None:
                response = await self._http_client.get(path, params=request_params)
            else:
                async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
                    response = await client.get(path, params=request_params)
        except httpx.TimeoutException as exc:
            logger.warning("ThingSpeak request timed out for path=%s", path)
            raise ThingSpeakTimeoutError("ThingSpeak request timed out.") from exc
        except httpx.RequestError as exc:
            logger.warning("ThingSpeak request failed for path=%s", path)
            raise ThingSpeakConnectionError("ThingSpeak connection failed.") from exc
        finally:
            request_logger.removeFilter(safe_filter)

        if response.status_code == 404:
            raise ThingSpeakHTTPError(404, "ThingSpeak channel or resource not found.")
        if response.status_code >= 400:
            raise ThingSpeakHTTPError(response.status_code, "ThingSpeak returned an unexpected status.")

        try:
            payload = response.json()
        except ValueError as exc:
            raise ThingSpeakInvalidResponseError("ThingSpeak returned invalid JSON.") from exc

        if not isinstance(payload, dict):
            raise ThingSpeakInvalidResponseError("ThingSpeak returned an unexpected JSON structure.")
        return payload

