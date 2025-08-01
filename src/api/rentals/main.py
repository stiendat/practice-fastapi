from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from datetime import date
from src.models.library_models import Rental, Book
from src.utils.db_utils import get_db

router = APIRouter()

@router.post("/rent")
async def rent_book(request: Request, db: Session = Depends(get_db)):
    rental_data = await request.json()
    user_id = rental_data.get("user_id")
    book_id = rental_data.get("book_id")

    if not user_id or not book_id:
        raise HTTPException(status_code=400, detail="Missing required fields")

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or book.quantity <= 0:
        raise HTTPException(status_code=400, detail="Book not available")

    rental = Rental(user_id=user_id, book_id=book_id, borrow_date=date.today())
    book.quantity -= 1
    db.add(rental)
    db.commit()
    db.refresh(rental)
    return {"id": rental.id, "user_id": rental.user_id, "book_id": rental.book_id, "borrow_date": rental.borrow_date}

@router.post("/return")
async def return_book(request: Request, db: Session = Depends(get_db)):
    return_data = await request.json()
    rental_id = return_data.get("rental_id")

    if not rental_id:
        raise HTTPException(status_code=400, detail="Missing required fields")

    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")

    book = db.query(Book).filter(Book.id == rental.book_id).first()
    book.quantity += 1
    rental.return_date = date.today()
    db.commit()
    return {"message": "Book returned successfully", "rental_id": rental.id, "return_date": rental.return_date}