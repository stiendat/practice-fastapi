from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession

from src.utils.db_utils import create_database_session, db_session_context
from src.dto import book_dto
from src.repository.book_repository import BookRepository

router = APIRouter()

@router.post("/books/", response_model=book_dto.BookDTO)
async def create_book(book: book_dto.BookCreateDTO, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await BookRepository().create(book)
    if not res:
        raise HTTPException(status_code=400, detail="Book creation failed")
    return res

@router.get("/all-books/", response_model=list[book_dto.BookDTO])
async def get_all_books(db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await BookRepository().get_all()
    if not res:
        raise HTTPException(status_code=404, detail="No books found")
    return res

@router.get("/books/", response_model=book_dto.BookDTO)
async def get_book_by_id(book_id: str, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await BookRepository().get_by_id(book_id)
    if not res:
        raise HTTPException(status_code=404, detail="Book not found")
    return res

@router.get("/books/field", response_model=list[book_dto.BookDTO])
async def get_books_by_field(field_name: str, value: str, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await BookRepository().get_by_field(field_name, value)
    if not res:
        raise HTTPException(status_code=404, detail=f"No books found with {field_name} = {value}")
    return res

@router.get("/books/field-int", response_model=list[book_dto.BookDTO])
async def get_books_by_field_int(field_name: str, value: int, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await BookRepository().get_by_field_int(field_name, value)
    if not res:
        raise HTTPException(status_code=404, detail=f"No books found with {field_name} = {value}")
    return res

@router.put("/books/{book_id}", response_model=book_dto.BookDTO)
async def update_book(book_id: str, book: book_dto.BookUpdateDTO, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await BookRepository().update(book_id, book)
    if not res:
        raise HTTPException(status_code=404, detail="Book not found or update failed")
    return res

@router.delete("/books/{book_id}",response_model=dict)
async def delete_book(book_id: str, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await BookRepository().delete(book_id)
    if not res:
        raise HTTPException(status_code=404, detail="Book not found or deletion failed")
    return {"detail": "Book deleted successfully"}