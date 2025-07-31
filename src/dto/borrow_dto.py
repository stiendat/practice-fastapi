from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field
from src.dto.base_dto import TimestampMixin
from uuid import UUID

class BorrowingCreateDTO(BaseModel):
    book_id: UUID
    user_id: UUID
    borrow_date: Optional[datetime] = None
    due_date: datetime

class BorrowingUpdateDTO(BaseModel):
    book_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    borrow_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    return_date: Optional[datetime] = None

class BorrowingDTO(TimestampMixin):
    id: UUID
    book_id: UUID
    user_id: UUID
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
