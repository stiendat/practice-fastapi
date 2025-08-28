"""
Book management API endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.library_models import get_async_session
from src.schemas.library_schemas import (
    BookResponse, BookCreate, BookUpdate, BooksListResponse,
    APIResponse, ErrorResponse
)
from src.services.library_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])


async def get_db():
    """Dependency to get async database session"""
    async with get_async_session() as db:
        yield db


@router.get("/", response_model=BooksListResponse)
async def get_books(
    skip: int = Query(0, ge=0, description="Number of books to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of books to return"),
    search: Optional[str] = Query(None, description="Search query for title or author"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of books with optional search and pagination
    """
    try:
        if search:
            books = await BookService.search_books(db, search, skip, limit)
        else:
            books = await BookService.get_books(db, skip, limit)
        
        return BooksListResponse(
            total=len(books),
            books=[BookResponse.model_validate(book) for book in books]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific book by ID
    """
    book = await BookService.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return BookResponse.model_validate(book)


@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new book
    """
    try:
        # Check if book with same ISBN already exists
        existing_book = await BookService.get_book_by_isbn(db, book.isbn)
        if existing_book:
            raise HTTPException(
                status_code=400, 
                detail=f"Book with ISBN {book.isbn} already exists"
            )
        
        db_book = await BookService.create_book(db, book)
        return BookResponse.model_validate(db_book)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create book: {str(e)}")


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int, 
    book_update: BookUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Update a book's information
    """
    try:
        # Check if updating ISBN to an existing one
        if book_update.isbn:
            existing_book = await BookService.get_book_by_isbn(db, book_update.isbn)
            if existing_book and existing_book.id != book_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Book with ISBN {book_update.isbn} already exists"
                )
        
        updated_book = await BookService.update_book(db, book_id, book_update)
        if not updated_book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        return BookResponse.model_validate(updated_book)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update book: {str(e)}")


@router.delete("/{book_id}", response_model=APIResponse)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a book (only if no active rentals exist)
    """
    try:
        success = await BookService.delete_book(db, book_id)
        if not success:
            # Check if book exists
            book = await BookService.get_book_by_id(db, book_id)
            if not book:
                raise HTTPException(status_code=404, detail="Book not found")
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot delete book with active rentals"
                )
        
        return APIResponse(
            success=True,
            message="Book deleted successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete book: {str(e)}")


@router.get("/{book_id}/availability")
async def check_book_availability(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Check if a book is available for rental
    """
    book = await BookService.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {
        "book_id": book.id,
        "title": book.title,
        "total_copies": book.total_copies,
        "available_copies": book.available_copies,
        "is_available": book.available_copies > 0
    }
