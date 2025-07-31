from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from src.db.database import get_db
from src.models.rental import Rental
from src.models.book import Book
from src.api.schemas.rentals import RentalCreate, RentalReturn, RentalOut

router = APIRouter(prefix="/rentals", tags=["Rentals"])


@router.post("/", response_model=RentalOut)
def create_rental(data: RentalCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == data.book_id).first()
    if not book or book.quantity <= 0:
        raise HTTPException(status_code=400, detail="Book not available")

    rental = Rental(
        user_id=data.user_id,
        book_id=data.book_id,
        due_date=data.due_date
    )

    # Trừ số lượng
    book.quantity -= 1

    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental


@router.post("/return", response_model=RentalOut)
def return_book(data: RentalReturn, db: Session = Depends(get_db)):
    rental = db.query(Rental).filter(Rental.id == data.rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")

    if rental.returned_at:
        raise HTTPException(status_code=400, detail="Book already returned")

    rental.returned_at = datetime.utcnow()

    # Tăng lại số lượng sách
    book = db.query(Book).filter(Book.id == rental.book_id).first()
    if book:
        book.quantity += 1

    db.commit()
    db.refresh(rental)
    return rental
