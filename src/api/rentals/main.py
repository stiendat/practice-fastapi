from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.utils.db_utils import create_database_session
from src.models.library_models import Rental, Book, User
from src.models.schemas import RentalResponse, RentalCreate, RentalReturn

router = APIRouter(prefix="/rentals", tags=["rentals"])


@router.post("/rent", response_model=RentalResponse)
async def rent_book(rental_data: RentalCreate, session: AsyncSession = Depends(create_database_session)):
    book_result = await session.execute(select(Book).where(Book.id == rental_data.book_id))
    book = book_result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.quantity <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    
    user_result = await session.execute(select(User).where(User.id == rental_data.user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_rental = await session.execute(
        select(Rental).where(
            and_(
                Rental.user_id == rental_data.user_id,
                Rental.book_id == rental_data.book_id,
                Rental.is_returned == False
            )
        )
    )
    
    if existing_rental.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already has this book rented")
    
    rental = Rental(
        user_id=rental_data.user_id,
        book_id=rental_data.book_id,
        rental_date=datetime.utcnow(),
        due_date=rental_data.due_date,
        is_returned=False
    )
    
    book.quantity -= 1
    
    session.add(rental)
    await session.commit()
    await session.refresh(rental)
    
    return rental


@router.post("/return", response_model=RentalResponse)
async def return_book(return_data: RentalReturn, session: AsyncSession = Depends(create_database_session)):
    rental = None
    
    if return_data.rental_id:
        result = await session.execute(select(Rental).where(Rental.id == return_data.rental_id))
        rental = result.scalar_one_or_none()
    elif return_data.book_id:
        result = await session.execute(
            select(Rental).where(
                and_(
                    Rental.book_id == return_data.book_id,
                    Rental.is_returned == False
                )
            )
        )
        rental = result.scalar_one_or_none()
    
    if not rental:
        raise HTTPException(status_code=404, detail="Active rental not found")
    
    if rental.is_returned:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    book_result = await session.execute(select(Book).where(Book.id == rental.book_id))
    book = book_result.scalar_one_or_none()
    
    rental.return_date = datetime.utcnow()
    rental.is_returned = True
    book.quantity += 1
    
    await session.commit()
    await session.refresh(rental)
    
    return rental