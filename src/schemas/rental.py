from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class RentalBase(BaseModel):
    user_id: str = Field(..., description="ID người mượn")
    book_id: str = Field(..., description="ID sách")
    expected_return_date: datetime = Field(..., description="Ngày dự kiến trả")


class RentalCreate(RentalBase):
    pass


class RentalReturn(BaseModel):
    book_id: str = Field(..., description="ID sách cần trả")


class RentalResponse(RentalBase):
    id: str = Field(..., description="ID giao dịch mượn")
    borrow_date: datetime = Field(..., description="Ngày mượn")
    actual_return_date: Optional[datetime] = Field(None, description="Ngày trả thực tế")
    status: str = Field(..., description="Trạng thái mượn")
    created_at: datetime = Field(..., description="Thời gian tạo")
    updated_at: Optional[datetime] = Field(None, description="Thời gian cập nhật")

    class Config:
        from_attributes = True 


class RentalListResponse(BaseModel):
    rentals: list[RentalResponse]
    total: int
    page: int = 1
    size: int = 10 