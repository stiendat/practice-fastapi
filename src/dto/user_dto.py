from typing import Optional

from pydantic import BaseModel, Field
from src.dto.base_dto import TimestampMixin
from uuid import UUID

class UserCreateDTO(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None


class UserUpdateDTO(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None

class UserDTO(TimestampMixin):
    id: UUID
    full_name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None