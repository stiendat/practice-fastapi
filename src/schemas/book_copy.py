from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from src.models.book_copy import BookCopyStatus

class BookCopyBase(BaseModel):
    book_id: int
    status: BookCopyStatus

class BookCopyCreate(BookCopyBase):
    pass

class BookCopyUpdate(BaseModel):
    """Schema for updating book copy (only status can be updated)"""
    status: BookCopyStatus

class BookCopyResponse(BookCopyBase):
    id: int
    created_at: datetime
    modified_at: datetime
    
    class Config:
        from_attributes = True

class BookCopyWithBookResponse(BaseModel):
    """Response model for book copy with basic book information"""
    # Book copy information
    id: int
    book_id: int
    status: BookCopyStatus
    created_at: datetime
    modified_at: datetime
    
    # Basic book information
    book_title: str
    book_author: str
    book_isbn: str
    
    class Config:
        from_attributes = True

class BookCopySearchQuery(BaseModel):
    """Search parameters for book copies"""
    book_id: Optional[int] = None
    status: Optional[BookCopyStatus] = None
    book_title: Optional[str] = None
    book_author: Optional[str] = None

class BookWithCopyResponse(BaseModel):
    """Response model for book information with copy details"""
    # Book information
    id: int
    ISBN: str
    title: str
    author: str
    publication_year: Optional[int] = None
    publisher: Optional[str] = None
    image_url_s: Optional[str] = None
    image_url_m: Optional[str] = None
    image_url_l: Optional[str] = None
    created_at: datetime
    modified_at: datetime
    
    # Book copy information
    copy_id: int
    copy_status: BookCopyStatus
    copy_created_at: datetime
    copy_modified_at: datetime
    
    class Config:
        from_attributes = True
