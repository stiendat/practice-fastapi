from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from src.schemas.book import BookCreate, BookResponse
from src.schemas.book_copy import BookWithCopyResponse, BookCopyResponse, BookCopyCreate
from src.models.book_copy import BookCopyStatus
from src.repositories.book_repository import BookRepository
from src.repositories.book_copy_repository import BookCopyRepository
from src.dependencies import get_book_repository, get_book_copy_repository

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
def get_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Get all books with pagination"""
    books = book_repo.get_all(skip=skip, limit=limit)
    return books

@router.get("/available", response_model=List[BookResponse])
def get_available_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Get books that have available copies for borrowing"""
    books = book_repo.get_available_books(skip=skip, limit=limit)
    return books

@router.get("/search", response_model=List[BookResponse])
def search_books(
    title: str = Query(None, description="Search by book title"),
    author: str = Query(None, description="Search by author name"),
    isbn: str = Query(None, description="Search by ISBN"),
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Search books by title, author, or ISBN"""
    if not any([title, author, isbn]):
        raise HTTPException(status_code=400, detail="At least one search parameter is required")
    
    books = book_repo.search_books(title=title, author=author, isbn=isbn)
    return books

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, book_repo: BookRepository = Depends(get_book_repository)):
    """Get a specific book by ID"""
    book = book_repo.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/isbn/{isbn}", response_model=BookResponse)
def get_book_by_isbn(isbn: str, book_repo: BookRepository = Depends(get_book_repository)):
    """Get a book by ISBN"""
    book = book_repo.get_by_isbn(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, book_repo: BookRepository = Depends(get_book_repository)):
    """Create a new book"""
    # Check if ISBN already exists
    existing_book = book_repo.get_by_isbn(book.ISBN)
    if existing_book:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    return book_repo.create(book)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int, 
    book: BookCreate, 
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Update a book"""
    db_book = book_repo.get(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if ISBN is being changed and if it conflicts with another book
    if book.ISBN != db_book.ISBN:
        existing_book = book_repo.get_by_isbn(book.ISBN)
        if existing_book:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    return book_repo.update(db_book, book)

@router.delete("/{book_id}")
def delete_book(book_id: int, book_repo: BookRepository = Depends(get_book_repository)):
    """Delete a book"""
    book = book_repo.delete(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {"message": "Book deleted successfully"}

@router.get("/copy/{book_copy_id}", response_model=BookWithCopyResponse)
def get_book_by_copy_id(book_copy_id: int, book_repo: BookRepository = Depends(get_book_repository)):
    """Get book information along with copy details by book_copy_id"""
    result = book_repo.get_book_by_copy_id(book_copy_id)
    if not result:
        raise HTTPException(status_code=404, detail="Book copy not found")
    
    book, book_copy = result
    
    # Create response with both book and copy information
    return BookWithCopyResponse(
        # Book information
        id=book.id,
        ISBN=book.ISBN,
        title=book.title,
        author=book.author,
        publication_year=book.publication_year,
        publisher=book.publisher,
        image_url_s=book.image_url_s,
        image_url_m=book.image_url_m,
        image_url_l=book.image_url_l,
        created_at=book.created_at,
        modified_at=book.modified_at,
        # Book copy information
        copy_id=book_copy.id,
        copy_status=book_copy.status,
        copy_created_at=book_copy.created_at,
        copy_modified_at=book_copy.modified_at
    )

@router.get("/{book_id}/copies", response_model=List[BookCopyResponse])
def get_book_copies(
    book_id: int,
    book_repo: BookRepository = Depends(get_book_repository),
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository)
):
    """Get all copies of a specific book"""
    # Verify book exists
    book = book_repo.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    copies = book_copy_repo.get_copies_by_book_id(book_id)
    return copies

@router.post("/{book_id}/copies", response_model=BookCopyResponse, status_code=201)
def create_book_copy_for_book(
    book_id: int,
    book_repo: BookRepository = Depends(get_book_repository),
    book_copy_repo: BookCopyRepository = Depends(get_book_copy_repository)
):
    """Create a new copy for a specific book"""
    # Verify book exists
    book = book_repo.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Create new copy with default available status
    copy_data = BookCopyCreate(book_id=book_id, status=BookCopyStatus.AVAILABLE)
    return book_copy_repo.create(copy_data)
