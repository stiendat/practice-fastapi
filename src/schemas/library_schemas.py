from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class RentalStatusEnum(str, Enum):
    RENTED = "RENTED"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"


# Base schemas
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=1, max_length=20)
    publication_year: Optional[int] = Field(None, ge=1000, le=9999)
    publisher: Optional[str] = Field(None, max_length=255)
    image_url_s: Optional[str] = Field(None, max_length=500)
    image_url_m: Optional[str] = Field(None, max_length=500)
    image_url_l: Optional[str] = Field(None, max_length=500)


class RentalBase(BaseModel):
    user_id: UUID
    book_id: UUID
    due_date: datetime


# Create schemas
class UserCreate(UserBase):
    pass


class BookCreate(BookBase):
    pass


class RentalCreate(BaseModel):
    user_id: UUID
    book_id: UUID
    days_to_return: int = Field(default=14, ge=1, le=365)


# Update schemas
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, min_length=1, max_length=20)
    publication_year: Optional[int] = Field(None, ge=1000, le=9999)
    publisher: Optional[str] = Field(None, max_length=255)
    image_url_s: Optional[str] = Field(None, max_length=500)
    image_url_m: Optional[str] = Field(None, max_length=500)
    image_url_l: Optional[str] = Field(None, max_length=500)
    is_available: Optional[bool] = None


# Response schemas
class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BookResponse(BookBase):
    id: UUID
    is_available: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RentalResponse(BaseModel):
    id: UUID
    user_id: UUID
    book_id: UUID
    rent_date: datetime
    return_date: Optional[datetime]
    due_date: datetime
    status: RentalStatusEnum
    created_at: datetime
    updated_at: datetime
    
    # Include related objects
    user: Optional[UserResponse] = None
    book: Optional[BookResponse] = None
    
    class Config:
        from_attributes = True


# List response schemas
class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int


class BookListResponse(BaseModel):
    books: list[BookResponse]
    total: int


class RentalListResponse(BaseModel):
    rentals: list[RentalResponse]
    total: int


# Return book schema
class ReturnBookRequest(BaseModel):
    rental_id: Optional[UUID] = None
    book_id: Optional[UUID] = None
    
    class Config:
        # At least one of rental_id or book_id must be provided
        validate_assignment = True
