from typing import Annotated, List
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from src.utils.db_utils import create_database_session
from src.models import Rental, User, Book
from .schemas import RentRequest, ReturnRequest, RentalResponse, RentalWithDetails

router = APIRouter(tags=["rentals"])


@router.post("/rent", response_model=RentalResponse, status_code=status.HTTP_201_CREATED)
async def rent_book(
    rent_data: RentRequest,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """Create a new book rental"""
    # Check if user exists
    user_result = await session.execute(
        select(User).where(User.id == rent_data.user_id)
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if book exists and is available
    book_result = await session.execute(
        select(Book).where(Book.id == rent_data.book_id)
    )
    book = book_result.scalar_one_or_none()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    if book.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is not available for rent"
        )
    
    # Check if user already has this book rented
    existing_rental = await session.execute(
        select(Rental).where(
            and_(
                Rental.user_id == rent_data.user_id,
                Rental.book_id == rent_data.book_id,
                Rental.status == "rented"
            )
        )
    )
    if existing_rental.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has this book rented"
        )
    
    # Create rental
    rental = Rental(
        user_id=rent_data.user_id,
        book_id=rent_data.book_id,
        expected_return_date=rent_data.expected_return_date
    )
    
    # Decrease book quantity
    book.quantity -= 1
    
    session.add(rental)
    await session.commit()
    await session.refresh(rental)
    
    return rental


@router.post("/return", response_model=RentalResponse)
async def return_book(
    return_data: ReturnRequest,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """Return a rented book"""
    rental = None
    
    # Find rental by rental_id if provided
    if return_data.rental_id:
        result = await session.execute(
            select(Rental).where(Rental.id == return_data.rental_id)
        )
        rental = result.scalar_one_or_none()
    
    # Find rental by book_id and user_id if rental_id not provided
    elif return_data.book_id and return_data.user_id:
        result = await session.execute(
            select(Rental).where(
                and_(
                    Rental.book_id == return_data.book_id,
                    Rental.user_id == return_data.user_id,
                    Rental.status == "rented"
                )
            )
        )
        rental = result.scalar_one_or_none()
    
    # Find rental by book_id only (latest rental for this book)
    elif return_data.book_id:
        result = await session.execute(
            select(Rental)
            .where(
                and_(
                    Rental.book_id == return_data.book_id,
                    Rental.status == "rented"
                )
            )
            .order_by(Rental.rent_date.desc())
        )
        rental = result.first()
        if rental:
            rental = rental[0]
    
    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active rental not found"
        )
    
    if rental.status == "returned":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book has already been returned"
        )
    
    # Update rental status
    rental.actual_return_date = datetime.utcnow()
    rental.status = "returned"
    
    # Increase book quantity
    book_result = await session.execute(
        select(Book).where(Book.id == rental.book_id)
    )
    book = book_result.scalar_one()
    book.quantity += 1
    
    await session.commit()
    await session.refresh(rental)
    
    return rental


@router.get("/rentals", response_model=List[RentalWithDetails])
async def get_rentals(
    session: Annotated[AsyncSession, Depends(create_database_session)],
    status_filter: str = None,
    skip: int = 0,
    limit: int = 100
):
    """Get all rentals with user and book details"""
    query = select(Rental).options(
        selectinload(Rental.user),
        selectinload(Rental.book)
    )
    
    if status_filter:
        query = query.where(Rental.status == status_filter)
    
    query = query.offset(skip).limit(limit).order_by(Rental.rent_date.desc())
    
    result = await session.execute(query)
    rentals = result.scalars().all()
    
    # Convert to response format with details
    rental_details = []
    for rental in rentals:
        rental_dict = {
            "id": rental.id,
            "user_id": rental.user_id,
            "book_id": rental.book_id,
            "rent_date": rental.rent_date,
            "expected_return_date": rental.expected_return_date,
            "actual_return_date": rental.actual_return_date,
            "status": rental.status,
            "user_name": rental.user.name if rental.user else None,
            "user_email": rental.user.email if rental.user else None,
            "book_title": rental.book.title if rental.book else None,
            "book_author": rental.book.author if rental.book else None,
            "book_isbn": rental.book.isbn if rental.book else None,
        }
        rental_details.append(rental_dict)
    
    return rental_details


@router.get("/rentals/{rental_id}", response_model=RentalWithDetails)
async def get_rental(
    rental_id: UUID,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """Get a specific rental by ID with details"""
    result = await session.execute(
        select(Rental)
        .options(selectinload(Rental.user), selectinload(Rental.book))
        .where(Rental.id == rental_id)
    )
    rental = result.scalar_one_or_none()
    
    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental not found"
        )
    
    return {
        "id": rental.id,
        "user_id": rental.user_id,
        "book_id": rental.book_id,
        "rent_date": rental.rent_date,
        "expected_return_date": rental.expected_return_date,
        "actual_return_date": rental.actual_return_date,
        "status": rental.status,
        "user_name": rental.user.name if rental.user else None,
        "user_email": rental.user.email if rental.user else None,
        "book_title": rental.book.title if rental.book else None,
        "book_author": rental.book.author if rental.book else None,
        "book_isbn": rental.book.isbn if rental.book else None,
    }
