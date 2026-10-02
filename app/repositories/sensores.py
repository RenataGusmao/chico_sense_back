from __future__ import annotations

import uuid

from sqlalchemy.orm import Session, joinedload

from app.models.iot import Sensor


class SensorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_with_dispositivo(self, sensor_id: uuid.UUID) -> Sensor | None:
        return (
            self.db.query(Sensor)
            .options(joinedload(Sensor.dispositivo))
            .filter(Sensor.id == sensor_id)
            .one_or_none()
        )

