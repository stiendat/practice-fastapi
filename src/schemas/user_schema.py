from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    rented_books: Optional[List[BookBase]] = []
    
    class Config:
        from_attributes = True