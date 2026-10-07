from fastapi import HTTPException


def invalid(message):
    raise HTTPException(422, message)


class CrudService:
    repository = None

    def __init__(self, db):
        self.db = db
        self.repo = self.repository(db)

    def get(self, record_id, lock=False):
        record = self.repo.get(record_id, lock)
        if record is None:
            raise HTTPException(404, "Registro nao encontrado.")
        return record

    def list(self, filters, limit=50, offset=0):
        return self.repo.list(filters, limit, offset)

    def validate(self, values, previous=None, changed=None):
        pass

    def create(self, data, **context):
        values = data.model_dump()
        values.update(context)
        self.validate(values)
        return self.repo.save(self.repo.model(**values))

    def update(self, record_id, data):
        record = self.get(record_id, lock=True)
        previous = self.repo.values(record)
        changed = data.model_dump(exclude_unset=True)
        values = previous | changed
        self.validate(values, previous, changed)
        for key in changed:
            setattr(record, key, values[key])
        # Validators may populate real timestamps on status transitions.
        for key in ("inicio_real", "chegada_em"):
            if key in values and values[key] != previous.get(key):
                setattr(record, key, values[key])
        return self.repo.save(record)
