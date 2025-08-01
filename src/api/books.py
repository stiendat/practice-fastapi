from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db_utils import create_database_session
from src.services.library_service import BookService
from src.schemas.library_schemas import (
    BookCreate, BookUpdate, BookResponse, BookListResponse
)

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=BookListResponse)
async def get_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    available_only: bool = Query(False, description="Filter only available books"),
    search: Optional[str] = Query(None, description="Search term for title, author, or publisher"),
    db: AsyncSession = Depends(create_database_session)
):
    """Get all books with pagination and filtering"""
    if search:
        books = await BookService.search_books(db, search, skip=skip, limit=limit)
    else:
        books = await BookService.get_all_books(db, skip=skip, limit=limit, available_only=available_only)
    
    return BookListResponse(books=books, total=len(books))


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: UUID,
    db: AsyncSession = Depends(create_database_session)
):
    """Get book by ID"""
    book = await BookService.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    book_data: BookCreate,
    db: AsyncSession = Depends(create_database_session)
):
    """Create a new book"""
    # Check if ISBN already exists
    existing_book = await BookService.get_book_by_isbn(db, book_data.isbn)
    if existing_book:
        raise HTTPException(status_code=400, detail="ISBN already exists")
    
    book = await BookService.create_book(db, book_data)
    return book


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: UUID,
    book_data: BookUpdate,
    db: AsyncSession = Depends(create_database_session)
):
    """Update book by ID"""
    # Check if ISBN is being updated and already exists
    if book_data.isbn:
        existing_book = await BookService.get_book_by_isbn(db, book_data.isbn)
        if existing_book and existing_book.id != book_id:
            raise HTTPException(status_code=400, detail="ISBN already exists")
    
    book = await BookService.update_book(db, book_id, book_data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: UUID,
    db: AsyncSession = Depends(create_database_session)
):
    """Delete book by ID"""
    success = await BookService.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
