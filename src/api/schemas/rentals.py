from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RentalCreate(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime


class RentalReturn(BaseModel):
    rental_id: int


class RentalOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: Optional[datetime]

    class Config:
        orm_mode = True
