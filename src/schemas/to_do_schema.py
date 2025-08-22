from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class TodoBase(BaseModel):
    title: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TodoUpdateResponse(TodoBase):
    id: UUID
    updated_at: datetime

    class Config:
        from_attributes = True