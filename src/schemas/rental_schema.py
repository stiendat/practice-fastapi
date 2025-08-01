from pydantic import BaseModel

class BookRentalCreate(BaseModel):
    user_id: int
    book_id: int

class BookRentalResponse(BaseModel):
    message: str
    book_id: int
    user_id: int