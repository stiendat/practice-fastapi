"""
Pydantic schemas for Library Management System API
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# Book Schemas
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, min_length=10, max_length=20)
    publication_year: Optional[int] = Field(None, ge=1000, le=2030)
    publisher: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    total_copies: int = Field(default=1, ge=1)
    image_url_s: Optional[str] = Field(None, max_length=500)
    image_url_m: Optional[str] = Field(None, max_length=500)
    image_url_l: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, min_length=10, max_length=20)
    publication_year: Optional[int] = Field(None, ge=1000, le=2030)
    publisher: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    total_copies: Optional[int] = Field(None, ge=1)
    image_url_s: Optional[str] = Field(None, max_length=500)
    image_url_m: Optional[str] = Field(None, max_length=500)
    image_url_l: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None


class BookResponse(BookBase):
    id: int
    available_copies: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# User Schemas
class UserBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Rental Schemas
class RentalBase(BaseModel):
    user_id: int = Field(..., gt=0)
    book_id: int = Field(..., gt=0)
    expected_return_date: date
    notes: Optional[str] = None


class RentalCreate(RentalBase):
    pass


class RentalUpdate(BaseModel):
    expected_return_date: Optional[date] = None
    notes: Optional[str] = None


class RentalReturn(BaseModel):
    actual_return_date: Optional[date] = None
    notes: Optional[str] = None


class RentalResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    rent_date: date
    expected_return_date: date
    actual_return_date: Optional[date]
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # Nested objects
    user: UserResponse
    book: BookResponse
    
    class Config:
        from_attributes = True


# Response Schemas for Lists
class BooksListResponse(BaseModel):
    total: int
    books: List[BookResponse]


class UsersListResponse(BaseModel):
    total: int
    users: List[UserResponse]


class RentalsListResponse(BaseModel):
    total: int
    rentals: List[RentalResponse]


# API Response Schemas
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[dict] = None
