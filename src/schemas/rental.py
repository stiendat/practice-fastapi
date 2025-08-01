from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class RentalItemBase(BaseModel):
    book_copy_id: int

class RentalItemCreate(RentalItemBase):
    pass

class RentalItemResponse(RentalItemBase):
    id: int
    rental_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RentalBase(BaseModel):
    user_id: int
    due_date: datetime
    rental_items: List[RentalItemCreate]

class RentalCreate(BaseModel):
    user_id: int
    book_ids: List[int]  # Simplified: just book IDs, system will find available copies
    due_date: Optional[datetime] = None  # If not provided, default to 14 days from now

class RentalResponse(BaseModel):
    id: int
    user_id: int
    rental_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    created_at: datetime
    modified_at: datetime
    rental_items: List[RentalItemResponse] = []

    class Config:
        from_attributes = True

class ReturnRequest(BaseModel):
    rental_id: Optional[int] = None
    book_copy_ids: Optional[List[int]] = None  # Alternative: return specific copies
