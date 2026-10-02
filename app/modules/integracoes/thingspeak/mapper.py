from __future__ import annotations

from decimal import Decimal, InvalidOperation

from app.modules.integracoes.thingspeak.schemas import (
    NormalizedThingSpeakReading,
    ThingSpeakFeed,
    ThingSpeakMappingConfig,
)


class ThingSpeakFieldMapper:
    def __init__(self, mapping_config: ThingSpeakMappingConfig) -> None:
        self.mapping_config = mapping_config

    def map_feed(self, channel_id: str, feed: ThingSpeakFeed) -> list[NormalizedThingSpeakReading]:
        readings: list[NormalizedThingSpeakReading] = []

        for field_name, value in sorted(feed.fields.items()):
            mapping = self.mapping_config.fields.get(field_name)
            if mapping is None:
                continue

            ignored_reason = None
            decimal_value = self._to_decimal(value)
            if value is None or value == "":
                ignored_reason = "empty_value"
            elif decimal_value is None:
                ignored_reason = "invalid_numeric_value"

            readings.append(
                NormalizedThingSpeakReading(
                    channel_id=channel_id,
                    entry_id=feed.entry_id,
                    field_name=field_name,
                    created_at=feed.created_at,
                    sensor_id=mapping.sensor_id,
                    tipo=mapping.tipo,
                    contexto=mapping.contexto,
                    unidade=mapping.unidade,
                    viagem_id=mapping.viagem_id,
                    carga_id=mapping.carga_id,
                    caixa_id=mapping.caixa_id,
                    valor=decimal_value,
                    valor_original=value,
                    ignorada=ignored_reason is not None,
                    motivo_ignorada=ignored_reason,
                )
            )

        return readings

    def map_feeds(self, channel_id: str, feeds: list[ThingSpeakFeed]) -> list[NormalizedThingSpeakReading]:
        readings: list[NormalizedThingSpeakReading] = []
        for feed in feeds:
            readings.extend(self.map_feed(channel_id, feed))
        return readings

    @staticmethod
    def _to_decimal(value: str | None) -> Decimal | None:
        if value is None or value == "":
            return None
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            return None
