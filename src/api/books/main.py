from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.utils.db_utils import create_database_session
from src.models.library_models import Book
from src.models.schemas import BookResponse, BookCreate

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[BookResponse])
async def get_all_books(session: AsyncSession = Depends(create_database_session)):
    result = await session.execute(select(Book))
    books = result.scalars().all()
    return books


@router.get("/{book_id}", response_model=BookResponse)
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(create_database_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book


@router.post("/", response_model=BookResponse)
async def create_book(book_data: BookCreate, session: AsyncSession = Depends(create_database_session)):
    book = Book(**book_data.model_dump())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book