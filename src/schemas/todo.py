from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Todo title")


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, description="Todo title")
    completed: Optional[bool] = Field(None, description="Todo completion status")


class TodoResponse(BaseModel):
    id: str
    title: str
    completed: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
