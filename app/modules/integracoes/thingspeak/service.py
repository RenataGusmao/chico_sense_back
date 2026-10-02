from __future__ import annotations

import json
import logging
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.enums import ContextoMedicao
from app.modules.integracoes.thingspeak.client import ThingSpeakClient
from app.modules.integracoes.thingspeak.exceptions import ThingSpeakConfigurationError
from app.modules.integracoes.thingspeak.mapper import ThingSpeakFieldMapper
from app.modules.integracoes.thingspeak.schemas import (
    NormalizedThingSpeakReading,
    ThingSpeakChannelConfig,
    ThingSpeakFeed,
    ThingSpeakMappingConfig,
    ThingSpeakMappingResult,
    ThingSpeakSyncError,
    ThingSpeakSyncSummary,
    ThingSpeakStatusResponse,
)
from app.repositories.integracoes import LeituraExternaRepository
from app.repositories.medicoes import MedicaoRepository
from app.repositories.sensores import SensorRepository

logger = logging.getLogger(__name__)


class ThingSpeakService:
    def __init__(
        self,
        config: ThingSpeakChannelConfig,
        client: ThingSpeakClient,
        mapper: ThingSpeakFieldMapper,
    ) -> None:
        self.config = config
        self.client = client
        self.mapper = mapper

    @classmethod
    def from_settings(cls) -> "ThingSpeakService":
        config = ThingSpeakChannelConfig(
            base_url=settings.thingspeak_base_url,
            channel_id=settings.thingspeak_channel_id,
            read_api_key=settings.thingspeak_read_api_key,
            timeout_seconds=settings.thingspeak_timeout_seconds,
        )
        mapping_config = ThingSpeakMappingConfig.from_raw_mapping(
            _load_mapping(settings.thingspeak_field_mapping_json)
        )
        return cls(
            config=config,
            client=ThingSpeakClient(
                base_url=config.base_url,
                read_api_key=config.read_api_key,
                timeout_seconds=config.timeout_seconds,
            ),
            mapper=ThingSpeakFieldMapper(mapping_config),
        )

    def get_status(self) -> ThingSpeakStatusResponse:
        configured = bool(self.config.channel_id)
        return ThingSpeakStatusResponse(
            configured=configured,
            base_url=self.config.base_url,
            channel_id=self.config.channel_id,
            message="ThingSpeak channel configured." if configured else "THINGSPEAK_CHANNEL_ID is not configured.",
        )

    async def get_feeds(self, results: int | None = None) -> list[ThingSpeakFeed]:
        channel_id = self._require_channel_id()
        logger.info("Starting ThingSpeak feeds query channel_id=%s", channel_id)
        response = await self.client.get_feeds(channel_id=channel_id, results=results)
        logger.info("ThingSpeak feeds received channel_id=%s count=%s", channel_id, len(response.feeds))
        return response.feeds

    async def get_latest_feed(self) -> ThingSpeakFeed | None:
        channel_id = self._require_channel_id()
        logger.info("Starting ThingSpeak latest feed query channel_id=%s", channel_id)
        feed = await self.client.get_latest_feed(channel_id=channel_id)
        logger.info("ThingSpeak latest feed received channel_id=%s found=%s", channel_id, feed is not None)
        return feed

    async def get_mapped_feeds(self, results: int | None = None) -> ThingSpeakMappingResult:
        channel_id = self._require_channel_id()
        feeds = await self.get_feeds(results=results)
        readings = self.mapper.map_feeds(channel_id=channel_id, feeds=feeds)
        ignored = sum(1 for reading in readings if reading.ignorada)
        logger.info(
            "ThingSpeak feeds processed channel_id=%s feeds=%s normalized=%s ignored=%s",
            channel_id,
            len(feeds),
            len(readings),
            ignored,
        )
        return ThingSpeakMappingResult(
            channel_id=channel_id,
            feeds_processados=len(feeds),
            leituras_normalizadas=readings,
            ignorados=ignored,
        )

    async def sincronizar_feeds(self, db: Session, results: int | None = None) -> ThingSpeakSyncSummary:
        channel_id = self._require_channel_id()
        logger.info("Starting ThingSpeak synchronization channel_id=%s", channel_id)

        feeds = await self.get_feeds(results=results)
        readings = self.mapper.map_feeds(channel_id=channel_id, feeds=feeds)
        summary = ThingSpeakSyncSummary(
            feeds_recebidos=len(feeds),
            fields_processados=len(readings),
            medicoes_criadas=0,
            duplicados=0,
            ignorados=0,
            erros=[],
        )

        sensores = SensorRepository(db)
        medicoes = MedicaoRepository(db)
        leituras_externas = LeituraExternaRepository(db)

        for reading in readings:
            error_reason = self._validate_reading(reading)
            if error_reason:
                self._ignore_reading(summary, reading, error_reason)
                continue

            if leituras_externas.exists(
                origem=reading.source.upper(),
                channel_id=reading.channel_id,
                entry_id=reading.entry_id,
                field_name=reading.field_name,
            ):
                summary.duplicados += 1
                continue

            sensor = sensores.get_with_dispositivo(reading.sensor_id)
            if sensor is None:
                self._ignore_reading(summary, reading, "sensor_not_found")
                continue

            viagem_id = reading.viagem_id or sensor.dispositivo.viagem_id
            carga_id = reading.carga_id or sensor.dispositivo.carga_id
            caixa_id = reading.caixa_id
            contexto = ContextoMedicao(reading.contexto)
            if contexto != ContextoMedicao.PROTOTIPO and (viagem_id is None or carga_id is None):
                self._ignore_reading(summary, reading, "missing_viagem_or_carga")
                continue

            try:
                with db.begin_nested():
                    medicao = medicoes.create(
                        sensor_id=reading.sensor_id,
                        viagem_id=viagem_id,
                        carga_id=carga_id,
                        caixa_id=caixa_id,
                        medida_em=reading.created_at,
                        contexto=contexto,
                        valor=reading.valor,
                        unidade=reading.unidade,
                    )
                    leituras_externas.create(
                        origem=reading.source.upper(),
                        channel_id=reading.channel_id,
                        entry_id=reading.entry_id,
                        field_name=reading.field_name,
                        medicao_id=medicao.id,
                    )
                summary.medicoes_criadas += 1
            except IntegrityError:
                summary.duplicados += 1
            except ValueError:
                self._ignore_reading(summary, reading, "invalid_contexto")
            except Exception as exc:
                logger.warning(
                    "ThingSpeak reading failed entry_id=%s field=%s reason=%s",
                    reading.entry_id,
                    reading.field_name,
                    exc.__class__.__name__,
                )
                self._ignore_reading(summary, reading, "persistence_error")

        db.commit()
        logger.info(
            "ThingSpeak synchronization finished channel_id=%s feeds=%s created=%s duplicated=%s ignored=%s",
            channel_id,
            summary.feeds_recebidos,
            summary.medicoes_criadas,
            summary.duplicados,
            summary.ignorados,
        )
        return summary

    def _require_channel_id(self) -> str:
        if not self.config.channel_id:
            raise ThingSpeakConfigurationError("THINGSPEAK_CHANNEL_ID is not configured.")
        return self.config.channel_id

    @staticmethod
    def _validate_reading(reading: NormalizedThingSpeakReading) -> str | None:
        if reading.sensor_id is None:
            return "missing_sensor_id"
        if not reading.contexto:
            return "missing_contexto"
        if not reading.unidade:
            return "missing_unidade"
        if reading.ignorada:
            return reading.motivo_ignorada or "invalid_value"
        if reading.valor is None:
            return "invalid_value"
        return None

    @staticmethod
    def _ignore_reading(
        summary: ThingSpeakSyncSummary,
        reading: NormalizedThingSpeakReading,
        reason: str,
    ) -> None:
        summary.ignorados += 1
        summary.erros.append(
            ThingSpeakSyncError(
                entry_id=reading.entry_id,
                field_name=reading.field_name,
                motivo=reason,
            )
        )


def _load_mapping(raw_mapping: str | None) -> dict[str, Any] | None:
    if not raw_mapping:
        return None
    try:
        loaded = json.loads(raw_mapping)
    except json.JSONDecodeError:
        logger.warning("Invalid THINGSPEAK_FIELD_MAPPING_JSON; using empty mapping.")
        return None
    if not isinstance(loaded, dict):
        logger.warning("THINGSPEAK_FIELD_MAPPING_JSON must be a JSON object; using empty mapping.")
        return None
    return loaded
