from typing import Optional

from pydantic import BaseModel, Field
from src.dto.base_dto import TimestampMixin
from uuid import UUID

class BookCreateDTO(BaseModel):
    ISBN: Optional[str] = None
    book_title: str
    book_author: Optional[str] = None
    year_of_publication: Optional[int] = None
    total_quantity: Optional[int] = None
    available_quantity: Optional[int] = None
    publisher: Optional[str] = None
    image_url_s: Optional[str] = None
    image_url_L: Optional[str] = None

class BookUpdateDTO(BaseModel):
    ISBN: Optional[str] = None
    book_title: Optional[str] = None
    book_author: Optional[str] = None
    year_of_publication: Optional[int] = None
    total_quantity: Optional[int] = None
    available_quantity: Optional[int] = None
    publisher: Optional[str] = None
    image_url_s: Optional[str] = None
    image_url_L: Optional[str] = None

class BookDTO(TimestampMixin):
    id: UUID
    ISBN: Optional[str] = None
    book_title: str
    book_author: Optional[str] = None
    year_of_publication: Optional[int] = None
    total_quantity: Optional[int] = None
    available_quantity: Optional[int] = None
    publisher: Optional[str] = None
    image_url_s: Optional[str] = None
    image_url_L: Optional[str] = None