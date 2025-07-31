from pydantic import BaseModel
from datetime import date
from typing import Optional


class BorrowBase(BaseModel):
    borrower_id: int
    book_id: int
    borrow_date: Optional[date] = None
    expected_return_date: Optional[date] = None


class BorrowCreate(BorrowBase):
    pass


class ReturnCreate(BaseModel):
    borrowing_id: int
    actual_return_date: Optional[date] = None


class BorrowResponse(BorrowBase):
    id: int
    actual_return_date: Optional[date] = None

    class Config:
        from_attributes = True
