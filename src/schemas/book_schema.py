from pydantic import BaseModel
from datetime import date
from typing import Optional

class BookBase(BaseModel):
    name: str
    author: str
    public_date: date

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    rented_by_id: Optional[int] = None
    
    class Config:
        from_attributes = True