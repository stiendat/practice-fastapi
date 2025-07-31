from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    isbn: str
    title: str
    author: Optional[str]
    year: Optional[int]
    publisher: Optional[str]
    image_url_s: Optional[str]
    image_url_m: Optional[str]
    image_url_l: Optional[str]

class BookOut(BookCreate):
    id: int

    class Config:
        orm_mode = True
