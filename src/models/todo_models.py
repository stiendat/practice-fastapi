from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1)
    completed: Optional[bool] = False

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    completed: Optional[bool]

class Todo(BaseModel):
    id: UUID
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }
