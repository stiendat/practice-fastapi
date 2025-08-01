"""
Library Management Pydantic Schemas
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=1, max_length=20)
    publication_year: Optional[int] = Field(None, ge=1000, le=9999)
    publisher: Optional[str] = Field(None, max_length=255)
    image_url_s: Optional[str] = Field(None, max_length=500)
    image_url_m: Optional[str] = Field(None, max_length=500)
    image_url_l: Optional[str] = Field(None, max_length=500)


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


class BookResponse(BaseModel):
    id: UUID
    title: str
    author: str
    isbn: str
    publication_year: Optional[int]
    publisher: Optional[str]
    image_url_s: Optional[str]
    image_url_m: Optional[str]
    image_url_l: Optional[str]
    is_available: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RentalCreate(BaseModel):
    user_id: UUID
    book_id: UUID
    days_to_return: int = Field(default=14, ge=1, le=365)


class RentalResponse(BaseModel):
    id: UUID
    user_id: UUID
    book_id: UUID
    rent_date: datetime
    return_date: Optional[datetime]
    due_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
