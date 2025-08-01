from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class BookBase(BaseModel):
    isbn: str
    title: str
    author: str
    year_of_publication: Optional[int] = None
    publisher: Optional[str] = None
    quantity: int = 1
    image_url_s: Optional[str] = None
    image_url_m: Optional[str] = None
    image_url_l: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    isbn: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    year_of_publication: Optional[int] = None
    publisher: Optional[str] = None
    quantity: Optional[int] = None
    image_url_s: Optional[str] = None
    image_url_m: Optional[str] = None
    image_url_l: Optional[str] = None


class BookResponse(BookBase):
    id: UUID

    class Config:
        from_attributes = True
