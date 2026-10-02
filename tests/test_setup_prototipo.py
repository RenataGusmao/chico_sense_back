from __future__ import annotations

import uuid
from typing import Any

from app.models.enums import ContextoMedicao, TipoSensor
from scripts.setup_prototipo import (
    DISPOSITIVO_IDENTIFICADOR,
    SENSOR_TEMPERATURA_IDENTIFICADOR,
    SENSOR_UMIDADE_IDENTIFICADOR,
    build_thingspeak_mapping,
    setup_prototipo,
)


class FakeQuery:
    def __init__(self, db: "FakeDB", model: type) -> None:
        self.db = db
        self.model = model
        self.filters: tuple[Any, ...] = ()

    def filter(self, *filters: Any) -> "FakeQuery":
        self.filters = filters
        return self

    def one_or_none(self) -> Any | None:
        if self.model.__name__ == "Dispositivo":
            return self._find_one(self.db.dispositivos.values())
        if self.model.__name__ == "Sensor":
            return self._find_one(self.db.sensores.values())
        return None

    def _find_one(self, objects: Any) -> Any | None:
        for obj in objects:
            if all(_matches_filter(obj, filter_expression) for filter_expression in self.filters):
                return obj
        return None


def _matches_filter(obj: Any, filter_expression: Any) -> bool:
    left = getattr(filter_expression, "left", None)
    right = getattr(filter_expression, "right", None)
    field_name = getattr(left, "key", None)
    expected_value = getattr(right, "value", None)
    if field_name is None:
        return False
    return getattr(obj, field_name) == expected_value


class FakeDB:
    def __init__(self) -> None:
        self.dispositivos: dict[str, Any] = {}
        self.sensores: dict[str, Any] = {}
        self.commits = 0

    def query(self, model: type) -> FakeQuery:
        return FakeQuery(self, model)

    def add(self, obj: Any) -> None:
        obj.id = uuid.uuid4()
        if obj.__class__.__name__ == "Dispositivo":
            self.dispositivos[obj.identificador] = obj
        elif obj.__class__.__name__ == "Sensor":
            self.sensores[obj.identificador] = obj

    def flush(self) -> None:
        return None

    def commit(self) -> None:
        self.commits += 1


def test_contexto_medicao_has_prototipo() -> None:
    assert ContextoMedicao.PROTOTIPO.value == "PROTOTIPO"


def test_setup_creates_device_and_two_sensors() -> None:
    db = FakeDB()

    result = setup_prototipo(db)

    assert result["dispositivo"].created is True
    assert result["sensor_temperatura"].created is True
    assert result["sensor_umidade"].created is True
    assert len(db.dispositivos) == 1
    assert len(db.sensores) == 2
    assert db.sensores[SENSOR_TEMPERATURA_IDENTIFICADOR].tipo == TipoSensor.TEMPERATURA
    assert db.sensores[SENSOR_UMIDADE_IDENTIFICADOR].tipo == TipoSensor.UMIDADE


def test_setup_second_execution_reuses_records_without_duplication() -> None:
    db = FakeDB()

    first = setup_prototipo(db)
    second = setup_prototipo(db)

    assert first["dispositivo"].created is True
    assert second["dispositivo"].created is False
    assert second["sensor_temperatura"].created is False
    assert second["sensor_umidade"].created is False
    assert len(db.dispositivos) == 1
    assert len(db.sensores) == 2


def test_mapping_uses_only_field1_and_field2() -> None:
    db = FakeDB()
    result = setup_prototipo(db)

    mapping = result["mapping"]

    assert set(mapping.keys()) == {"field1", "field2"}
    assert mapping["field1"]["contexto"] == "PROTOTIPO"
    assert mapping["field2"]["contexto"] == "PROTOTIPO"
    assert "field3" not in mapping
    assert "field4" not in mapping
    assert "field5" not in mapping


def test_build_mapping_has_expected_sensor_ids() -> None:
    db = FakeDB()
    result = setup_prototipo(db)
    temperatura = result["sensor_temperatura"].obj
    umidade = result["sensor_umidade"].obj

    mapping = build_thingspeak_mapping(temperatura, umidade)

    assert mapping["field1"]["sensor_id"] == str(temperatura.id)
    assert mapping["field2"]["sensor_id"] == str(umidade.id)
