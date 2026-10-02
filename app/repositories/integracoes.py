from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models.integracoes import LeituraExterna


class LeituraExternaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def exists(self, *, origem: str, channel_id: str, entry_id: int, field_name: str) -> bool:
        return (
            self.db.query(LeituraExterna.id)
            .filter(
                LeituraExterna.origem == origem,
                LeituraExterna.channel_id == channel_id,
                LeituraExterna.entry_id == entry_id,
                LeituraExterna.field_name == field_name,
            )
            .first()
            is not None
        )

    def create(
        self,
        *,
        origem: str,
        channel_id: str,
        entry_id: int,
        field_name: str,
        medicao_id: uuid.UUID,
    ) -> LeituraExterna:
        leitura = LeituraExterna(
            origem=origem,
            channel_id=channel_id,
            entry_id=entry_id,
            field_name=field_name,
            medicao_id=medicao_id,
        )
        self.db.add(leitura)
        self.db.flush()
        return leitura

