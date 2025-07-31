from pydantic import BaseModel
from typing import Optional


class BookBase(BaseModel):
    isbn: str
    title: str
    author: str
    year_of_publication: int
    publisher: str
    img_url_s: Optional[str] = None
    img_url_m: Optional[str] = None
    img_url_l: Optional[str] = None
    total_quantity: int
    available_quantity: int


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
