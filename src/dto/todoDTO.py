import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from src.dto.timestampmixin import TimestampMixin

class TodoCreateDTO(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    completed: Optional[bool] = False

class TodoUpdateDTO(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: Optional[str] = None
    completed: Optional[bool] = None
    
    @model_validator(mode='after')
    def check_at_least_one_field(self):
        if self.title is None and self.completed is None:
            raise ValueError("At least one field (title or completed) must be provided")
        return self

class TodoDTO(TimestampMixin):
    id: UUID = Field(default_factory=uuid4)
    title: str
    completed: bool = False
    