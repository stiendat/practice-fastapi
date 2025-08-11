from pydantic import BaseModel, model_validator
from src.dto.base_dto import TimestampMixin
from uuid import UUID
from typing import Optional


class TodoDTO(TimestampMixin):
    id: UUID
    title: str
    completed: bool

class TodoCreateDTO(BaseModel):
    title: str
    completed: Optional[bool] = False

class TodoUpdateDTO(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

    @model_validator(mode="before")
    @classmethod
    def validate_at_least_one_field(cls, values):
        if not any(values.values() if isinstance(values, dict) else []):
            raise ValueError("At least one field must be provided")
        return values
