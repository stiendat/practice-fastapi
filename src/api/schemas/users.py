from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str]


class UserOut(UserCreate):
    id: int

    class Config:
        orm_mode = True
