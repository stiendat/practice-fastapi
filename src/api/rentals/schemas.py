from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class RentRequest(BaseModel):
    user_id: UUID
    book_id: UUID
    expected_return_date: Optional[datetime] = None


class ReturnRequest(BaseModel):
    rental_id: Optional[UUID] = None
    book_id: Optional[UUID] = None
    user_id: Optional[UUID] = None


class RentalResponse(BaseModel):
    id: UUID
    user_id: UUID
    book_id: UUID
    rent_date: datetime
    expected_return_date: datetime
    actual_return_date: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True


class RentalWithDetails(RentalResponse):
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    book_title: Optional[str] = None
    book_author: Optional[str] = None
    book_isbn: Optional[str] = None
