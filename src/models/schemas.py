from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    year: int
    quantity: int


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    full_name: str
    email: str  # Temporarily using str instead of EmailStr
    phone: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True


class RentalBase(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime


class RentalCreate(RentalBase):
    pass


class RentalResponse(RentalBase):
    id: int
    rental_date: datetime
    return_date: Optional[datetime] = None
    is_returned: bool
    
    class Config:
        from_attributes = True


class RentalReturn(BaseModel):
    rental_id: Optional[int] = None
    book_id: Optional[int] = None