from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500, description="Tên sách")
    author: str = Field(..., min_length=1, max_length=200, description="Tác giả")
    year_of_publication: Optional[int] = Field(None, ge=1900, le=2024, description="Năm xuất bản")
    publisher: Optional[str] = Field(None, max_length=200, description="Nhà xuất bản")
    image_url_s: Optional[str] = Field(None, description="URL hình ảnh nhỏ")
    image_url_m: Optional[str] = Field(None, description="URL hình ảnh vừa")
    image_url_l: Optional[str] = Field(None, description="URL hình ảnh lớn")
    quantity: int = Field(1, ge=0, description="Số lượng sách có sẵn")


class BookCreate(BookBase):
    id: str = Field(..., min_length=1, max_length=13, description="ISBN của sách")


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=200)
    year_of_publication: Optional[int] = Field(None, ge=1900, le=2024)
    publisher: Optional[str] = Field(None, max_length=200)
    image_url_s: Optional[str] = None
    image_url_m: Optional[str] = None
    image_url_l: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)


class BookResponse(BookBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BookListResponse(BaseModel):
    books: list[BookResponse]
    total: int
    page: int = 1
    size: int = 10 