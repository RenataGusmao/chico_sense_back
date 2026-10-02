from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.enums import ContextoMedicao
from app.models.iot import Medicao


class MedicaoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        sensor_id: uuid.UUID,
        viagem_id: uuid.UUID | None,
        carga_id: uuid.UUID | None,
        caixa_id: uuid.UUID | None,
        medida_em: datetime,
        contexto: ContextoMedicao,
        valor: Decimal,
        unidade: str,
    ) -> Medicao:
        medicao = Medicao(
            sensor_id=sensor_id,
            viagem_id=viagem_id,
            carga_id=carga_id,
            caixa_id=caixa_id,
            medida_em=medida_em,
            contexto=contexto,
            valor=valor,
            unidade=unidade,
        )
        self.db.add(medicao)
        self.db.flush()
        return medicao
