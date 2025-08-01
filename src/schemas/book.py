from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class BookBase(BaseModel):
    ISBN: str
    title: str
    author: str
    publication_year: Optional[int] = None
    publisher: Optional[str] = None
    image_url_s: Optional[str] = None
    image_url_m: Optional[str] = None  
    image_url_l: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    created_at: datetime
    modified_at: datetime
    
    class Config:
        from_attributes = True

class BookSearchQuery(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
