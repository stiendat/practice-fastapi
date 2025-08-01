from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Book, User
from src.schemas.rental_schema import BookRentalCreate, BookRentalResponse
from src.utils.db_utils import create_database_session

router = APIRouter(prefix="/rentals", tags=["rentals"])

@router.post("/", response_model=BookRentalResponse)
async def rent_book(
    rental: BookRentalCreate,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """
    Rent a book to a user
    """
    # Check if the user exists
    result = await session.execute(select(User).filter(User.id == rental.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {rental.user_id} not found"
        )
    
    # Check if the book exists
    result = await session.execute(select(Book).filter(Book.id == rental.book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {rental.book_id} not found"
        )
    
    # Check if the book is already rented
    if book.rented_by_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with ID {rental.book_id} is already rented"
        )
    
    # Rent the book to the user
    book.rented_by_id = rental.user_id
    await session.commit()
    await session.refresh(book)
    
    return BookRentalResponse(
        message="Book rented successfully",
        book_id=book.id,
        user_id=user.id
    )

@router.delete("/{book_id}", response_model=BookRentalResponse)
async def return_book(
    book_id: int,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """
    Return a rented book
    """
    # Check if the book exists
    result = await session.execute(select(Book).filter(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    
    # Check if the book is actually rented
    if book.rented_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with ID {book_id} is not currently rented"
        )
    
    user_id = book.rented_by_id
    
    # Return the book (remove the rental)
    book.rented_by_id = None
    await session.commit()
    await session.refresh(book)
    
    return BookRentalResponse(
        message="Book returned successfully",
        book_id=book.id,
        user_id=user_id
    )

@router.get("/user/{user_id}", response_model=list[int])
async def get_user_rented_books(
    user_id: int,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """
    Get all books rented by a user
    """
    # Check if the user exists
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Get all books rented by the user
    result = await session.execute(select(Book.id).filter(Book.rented_by_id == user_id))
    rented_book_ids = result.scalars().all()
    
    return rented_book_ids