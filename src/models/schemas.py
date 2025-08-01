from pydantic import BaseModel
import datetime
import uuid
from typing import Optional

# --- Book Schemas ---
class BookBase(BaseModel):
    """Base schema for book properties."""
    title: str
    author: str
    published_date: Optional[str] = None
    publisher: Optional[str] = None
    version: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None

class BookCreate(BookBase):
    """Schema for creating a new book."""
    pass

class BookRead(BookBase):
    """Schema for reading book data, including generated fields."""
    id: uuid.UUID
    created_at: datetime.datetime
    modified_at: datetime.datetime

    class Config:
        """Enables ORM mode for seamless conversion from SQLAlchemy models."""
        orm_mode = True

# --- User Schemas ---
class UserBase(BaseModel):
    """Base schema for user properties."""
    username: str
    email: str
    phone: str
    address: str

class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass

class UserRead(UserBase):
    """Schema for reading user data, including generated fields."""
    id: uuid.UUID
    created_at: datetime.datetime
    modified_at: datetime.datetime

    class Config:
        """Enables ORM mode for seamless conversion from SQLAlchemy models."""
        orm_mode = True

# --- Rental Schemas ---
class RentalCreate(BaseModel):
    """Schema for creating a new book rental."""
    book_id: uuid.UUID
    user_id: uuid.UUID
    volume: int

class RentalRead(BaseModel):
    """Schema for reading book rental data, including generated fields."""
    id: int
    book_id: uuid.UUID
    user_id: uuid.UUID
    rental_date: datetime.datetime
    expected_return_date: datetime.datetime
    volume: int

    class Config:
        """Enables ORM mode for seamless conversion from SQLAlchemy models."""
        orm_mode = True