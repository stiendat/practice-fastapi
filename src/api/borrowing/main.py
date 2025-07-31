from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date
from typing import Optional

from src.models import Borrowing, Book, Borrower
from src.utils.db_utils import create_database_session
from src.api.borrowing.schemas import BorrowCreate, ReturnCreate, BorrowResponse

router = APIRouter(prefix="/borrowing", tags=["borrowing"])


@router.post("/rent", response_model=BorrowResponse, status_code=status.HTTP_201_CREATED)
async def rent_book(borrow_data: BorrowCreate, session: AsyncSession = Depends(create_database_session)):
    # Check if borrower exists
    borrower_result = await session.execute(select(Borrower).where(Borrower.id == borrow_data.borrower_id))
    borrower = borrower_result.scalar_one_or_none()

    if not borrower:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Borrower with id {borrow_data.borrower_id} not found"
        )

    # Check if book exists
    book_result = await session.execute(select(Book).where(Book.id == borrow_data.book_id))
    book = book_result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {borrow_data.book_id} not found"
        )

    # Check if book is available
    if book.available_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with id {borrow_data.book_id} is not available for borrowing"
        )

    # Create new borrowing record
    new_borrowing = Borrowing(
        borrower_id=borrow_data.borrower_id,
        book_id=borrow_data.book_id,
        borrow_date=borrow_data.borrow_date or date.today(),
        expected_return_date=borrow_data.expected_return_date
    )

    # Update book availability
    book.available_quantity -= 1

    session.add(new_borrowing)
    await session.commit()
    await session.refresh(new_borrowing)

    return new_borrowing


@router.post("/return", response_model=BorrowResponse)
async def return_book(return_data: ReturnCreate, session: AsyncSession = Depends(create_database_session)):
    # Check if borrowing record exists
    borrowing_result = await session.execute(
        select(Borrowing).where(Borrowing.id == return_data.borrowing_id)
    )
    borrowing = borrowing_result.scalar_one_or_none()

    if not borrowing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Borrowing record with id {return_data.borrowing_id} not found"
        )

    # Check if book is already returned
    if borrowing.actual_return_date is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book is already returned"
        )

    # Update borrowing record with actual return date
    borrowing.actual_return_date = return_data.actual_return_date or date.today()

    # Update book availability
    book_result = await session.execute(select(Book).where(Book.id == borrowing.book_id))
    book = book_result.scalar_one_or_none()
    if book:
        book.available_quantity += 1

    await session.commit()
    await session.refresh(borrowing)

    return borrowing
