from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class Repository:
    model = None

    def __init__(self, db: Session):
        self.db = db

    def get(self, record_id: UUID, lock: bool = False):
        query = select(self.model).where(self.model.id == record_id)
        if lock:
            query = query.with_for_update().execution_options(populate_existing=True)
        return self.db.scalar(query)

    def list(self, filters: dict, limit: int, offset: int):
        query = select(self.model)
        for name, value in filters.items():
            if value is not None:
                query = query.where(getattr(self.model, name) == value)
        return list(self.db.scalars(query.order_by(self.model.created_at, self.model.id).limit(limit).offset(offset)))

    def values(self, record):
        return {column.key: getattr(record, column.key) for column in inspect(self.model).columns}

    def save(self, record):
        self.db.add(record)
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(409, "Identificador duplicado ou relacionamento invalido.") from exc
        self.db.refresh(record)
        return record
