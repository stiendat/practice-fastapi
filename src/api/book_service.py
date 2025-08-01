from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Book
from src.schemas.book_schema import BookCreate, BookResponse
from src.utils.db_utils import create_database_session

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
async def get_books(
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """
    Get all books from the database
    """
    result = await session.execute(select(Book))
    books = result.scalars().all()
    return books

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int, 
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """
    Get a specific book by ID
    """
    result = await session.execute(select(Book).filter(Book.id == book_id))
    book = result.scalars().first()
    
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreate,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """
    Create a new book
    """
    new_book = Book(
        name=book.name,
        author=book.author,
        public_date=book.public_date
    )
    
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    
    return new_book