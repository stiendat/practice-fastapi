from pydantic import BaseModel
from typing import Optional


class BorrowerBase(BaseModel):
    full_name: str
    email: str
    phone_number: Optional[str] = None


class BorrowerCreate(BorrowerBase):
    pass


class BorrowerResponse(BorrowerBase):
    id: int

    class Config:
        from_attributes = True
