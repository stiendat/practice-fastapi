from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from src.schemas.book_copy import (
    BookCopyCreate, BookCopyUpdate, BookCopyResponse, 
    BookCopyWithBookResponse, BookCopySearchQuery
)
from src.models.book_copy import BookCopyStatus
from src.repositories.book_copy_repository import BookCopyRepository
from src.repositories.book_repository import BookRepository
from src.dependencies import get_book_copy_repository, get_book_repository

router = APIRouter(prefix="/book-copies", tags=["book-copies"])

@router.get("/", response_model=List[BookCopyResponse])
def get_book_copies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository)
):
    """Get all book copies with pagination"""
    copies = book_copy_repo.get_all(skip=skip, limit=limit)
    return copies

@router.get("/search", response_model=List[BookCopyWithBookResponse])
def search_book_copies(
    book_id: Optional[int] = Query(None, description="Filter by book ID"),
    status: Optional[BookCopyStatus] = Query(None, description="Filter by copy status"),
    book_title: Optional[str] = Query(None, description="Search by book title"),
    book_author: Optional[str] = Query(None, description="Search by book author"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository)
):
    """Search book copies with various filters"""
    copies = book_copy_repo.search_copies(
        book_id=book_id,
        status=status,
        book_title=book_title,
        book_author=book_author,
        skip=skip,
        limit=limit
    )
    
    # Transform to include book information
    result = []
    for copy in copies:
        result.append(BookCopyWithBookResponse(
            id=copy.id,
            book_id=copy.book_id,
            status=copy.status,
            created_at=copy.created_at,
            modified_at=copy.modified_at,
            book_title=copy.book.title,
            book_author=copy.book.author,
            book_isbn=copy.book.ISBN
        ))
    
    return result

@router.get("/by-status/{status}", response_model=List[BookCopyResponse])
def get_copies_by_status(
    status: BookCopyStatus,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository)
):
    """Get book copies by status"""
    copies = book_copy_repo.get_copies_by_status(status, skip=skip, limit=limit)
    return copies

@router.get("/book/{book_id}", response_model=List[BookCopyResponse])
def get_copies_by_book_id(
    book_id: int,
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository)
):
    """Get all copies of a specific book"""
    copies = book_copy_repo.get_copies_by_book_id(book_id)
    return copies

@router.get("/book/{book_id}/available", response_model=List[BookCopyResponse])
def get_available_copies_by_book_id(
    book_id: int,
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository)
):
    """Get available copies of a specific book"""
    copies = book_copy_repo.get_available_copies_by_book_id(book_id)
    return copies

@router.get("/{copy_id}", response_model=BookCopyResponse)
def get_book_copy(
    copy_id: int,
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository)
):
    """Get a specific book copy by ID"""
    copy = book_copy_repo.get(copy_id)
    if not copy:
        raise HTTPException(status_code=404, detail="Book copy not found")
    return copy

@router.post("/", response_model=BookCopyResponse, status_code=201)
def create_book_copy(
    copy: BookCopyCreate,
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository),
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Create a new book copy"""
    # Verify that the book exists
    book = book_repo.get(copy.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book_copy_repo.create(copy)

@router.put("/{copy_id}", response_model=BookCopyResponse)
def update_book_copy(
    copy_id: int,
    copy_update: BookCopyUpdate,
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository)
):
    """Update a book copy (mainly status updates)"""
    db_copy = book_copy_repo.get(copy_id)
    if not db_copy:
        raise HTTPException(status_code=404, detail="Book copy not found")
    
    return book_copy_repo.update(db_copy, copy_update)

@router.patch("/{copy_id}/status", response_model=BookCopyResponse)
def update_copy_status(
    copy_id: int,
    new_status: BookCopyStatus,
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository)
):
    """Update only the status of a book copy"""
    copy = book_copy_repo.update_status(copy_id, new_status)
    if not copy:
        raise HTTPException(status_code=404, detail="Book copy not found")
    return copy

@router.delete("/{copy_id}")
def delete_book_copy(
    copy_id: int,
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository)
):
    """Delete a book copy"""
    copy = book_copy_repo.delete(copy_id)
    if not copy:
        raise HTTPException(status_code=404, detail="Book copy not found")
    
    return {"message": "Book copy deleted successfully"}

@router.get("/stats/book/{book_id}")
def get_book_copy_stats(
    book_id: int,
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository),
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Get statistics of book copies for a specific book"""
    # Verify book exists
    book = book_repo.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    stats = {
        "book_id": book_id,
        "book_title": book.title,
        "total_copies": 0,
        "available": 0,
        "borrowed": 0,
        "lost": 0,
        "damaged": 0
    }
    
    # Count copies by status
    for status in BookCopyStatus:
        count = book_copy_repo.count_by_book_and_status(book_id, status)
        stats[status.value] = count
        stats["total_copies"] += count
    
    return stats
