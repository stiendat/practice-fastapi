from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class TodoCreate(BaseModel):
    title: str
    completed: Optional[bool] = False

class TodoUpdate(BaseModel):
    title: Optional[str]
    completed: Optional[bool]

class Todo(BaseModel):
    id: UUID
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime
