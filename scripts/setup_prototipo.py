from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.enums import ContextoMedicao, StatusDispositivo, StatusSensor, TipoSensor
from app.models.iot import Dispositivo, Sensor

DISPOSITIVO_IDENTIFICADOR = "sensor-prototipo-sala"
DISPOSITIVO_DESCRICAO = "Dispositivo utilizado para validação acadêmica da integração IoT do ChicoSense."
SENSOR_TEMPERATURA_IDENTIFICADOR = "sensor-temperatura-prototipo-sala"
SENSOR_UMIDADE_IDENTIFICADOR = "sensor-umidade-prototipo-sala"


@dataclass(frozen=True)
class SetupItemResult:
    obj: Any
    created: bool

    @property
    def status(self) -> str:
        return "criado" if self.created else "reutilizado"


def get_or_create_dispositivo(db: Session) -> SetupItemResult:
    dispositivo = (
        db.query(Dispositivo)
        .filter(Dispositivo.identificador == DISPOSITIVO_IDENTIFICADOR)
        .one_or_none()
    )
    if dispositivo is not None:
        return SetupItemResult(dispositivo, created=False)

    dispositivo = Dispositivo(
        identificador=DISPOSITIVO_IDENTIFICADOR,
        descricao=DISPOSITIVO_DESCRICAO,
        status=StatusDispositivo.ATIVO,
    )
    db.add(dispositivo)
    db.flush()
    return SetupItemResult(dispositivo, created=True)


def get_or_create_sensor(
    db: Session,
    *,
    dispositivo: Dispositivo,
    identificador: str,
    tipo: TipoSensor,
    unidade: str,
) -> SetupItemResult:
    sensor = (
        db.query(Sensor)
        .filter(
            Sensor.dispositivo_id == dispositivo.id,
            Sensor.identificador == identificador,
        )
        .one_or_none()
    )
    if sensor is not None:
        return SetupItemResult(sensor, created=False)

    sensor = Sensor(
        dispositivo_id=dispositivo.id,
        identificador=identificador,
        tipo=tipo,
        contexto=ContextoMedicao.PROTOTIPO,
        unidade=unidade,
        status=StatusSensor.ATIVO,
    )
    db.add(sensor)
    db.flush()
    return SetupItemResult(sensor, created=True)


def build_thingspeak_mapping(sensor_temperatura: Sensor, sensor_umidade: Sensor) -> dict[str, dict[str, str]]:
    return {
        "field1": {
            "sensor_id": str(sensor_temperatura.id),
            "tipo": TipoSensor.TEMPERATURA.value,
            "contexto": ContextoMedicao.PROTOTIPO.value,
            "unidade": sensor_temperatura.unidade,
        },
        "field2": {
            "sensor_id": str(sensor_umidade.id),
            "tipo": TipoSensor.UMIDADE.value,
            "contexto": ContextoMedicao.PROTOTIPO.value,
            "unidade": sensor_umidade.unidade,
        },
    }


def setup_prototipo(db: Session) -> dict[str, Any]:
    dispositivo_result = get_or_create_dispositivo(db)
    temperatura_result = get_or_create_sensor(
        db,
        dispositivo=dispositivo_result.obj,
        identificador=SENSOR_TEMPERATURA_IDENTIFICADOR,
        tipo=TipoSensor.TEMPERATURA,
        unidade="C",
    )
    umidade_result = get_or_create_sensor(
        db,
        dispositivo=dispositivo_result.obj,
        identificador=SENSOR_UMIDADE_IDENTIFICADOR,
        tipo=TipoSensor.UMIDADE,
        unidade="%",
    )
    db.commit()

    mapping = build_thingspeak_mapping(temperatura_result.obj, umidade_result.obj)
    return {
        "dispositivo": dispositivo_result,
        "sensor_temperatura": temperatura_result,
        "sensor_umidade": umidade_result,
        "mapping": mapping,
    }


def print_setup_result(result: dict[str, Any]) -> None:
    dispositivo = result["dispositivo"]
    sensor_temperatura = result["sensor_temperatura"]
    sensor_umidade = result["sensor_umidade"]

    print("Setup do protótipo ChicoSense concluído.")
    print(f"Dispositivo: {dispositivo.status} | id={dispositivo.obj.id}")
    print(f"Sensor de Temperatura: {sensor_temperatura.status} | id={sensor_temperatura.obj.id}")
    print(f"Sensor de Umidade: {sensor_umidade.status} | id={sensor_umidade.obj.id}")
    print()
    print("Configure no .env:")
    print("THINGSPEAK_CHANNEL_ID=3493148")
    print("THINGSPEAK_READ_API_KEY=<chave real>")
    print("THINGSPEAK_FIELD_MAPPING_JSON=")
    print(json.dumps(result["mapping"], ensure_ascii=False))
    print()
    print("Observação: field3, field4 e field5 são estatísticas derivadas e não entram em medicoes.")


def main() -> None:
    db = SessionLocal()
    try:
        result = setup_prototipo(db)
        print_setup_result(result)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

