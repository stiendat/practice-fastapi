from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from src.models import Book
from src.utils.db_utils import create_database_session
from src.api.books.schemas import BookCreate, BookResponse

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[BookResponse])
async def get_books(session: AsyncSession = Depends(create_database_session)):
    result = await session.execute(select(Book))
    books = result.scalars().all()
    return books


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, session: AsyncSession = Depends(create_database_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )

    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreate, session: AsyncSession = Depends(create_database_session)):
    result = await session.execute(select(Book).where(Book.isbn == book_data.isbn))
    existing_book = result.scalar_one_or_none()

    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with ISBN {book_data.isbn} already exists"
        )

    new_book = Book(**book_data.dict())
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book
