from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, allow_inf_nan=False)


class Update(Input):
    @model_validator(mode="after")
    def reject_required_null(self):
        required = getattr(type(self), "required_fields", ())
        if any(field in self.model_fields_set and getattr(self, field) is None for field in required):
            raise ValueError("Required fields cannot be null")
        return self


class Response(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    updated_at: datetime
