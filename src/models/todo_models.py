from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from src.utils.db_utils import Base


# ORM model for Postgres (async compatible)
class Todo(Base):
    __tablename__ = "todos"

    id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Pydantic schemas
class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id: UUID
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
