from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.utils.db_utils import create_database_session
from src.models import Book
from .schemas import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[BookResponse])
async def get_books(
    session: Annotated[AsyncSession, Depends(create_database_session)],
    skip: int = 0,
    limit: int = 100
):
    """Get all books with pagination"""
    result = await session.execute(
        select(Book).offset(skip).limit(limit)
    )
    books = result.scalars().all()
    return books


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: UUID,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """Get a specific book by ID"""
    result = await session.execute(
        select(Book).where(Book.id == book_id)
    )
    book = result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """Create a new book"""
    try:
        book = Book(**book_data.model_dump())
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this ISBN already exists"
        )


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: UUID,
    book_data: BookUpdate,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """Update a book"""
    result = await session.execute(
        select(Book).where(Book.id == book_id)
    )
    book = result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Update only provided fields
    update_data = book_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)
    
    try:
        await session.commit()
        await session.refresh(book)
        return book
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this ISBN already exists"
        )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: UUID,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """Delete a book"""
    result = await session.execute(
        select(Book).where(Book.id == book_id)
    )
    book = result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    await session.delete(book)
    await session.commit()
