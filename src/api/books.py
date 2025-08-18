from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db_utils import create_database_session
from src.services.book_service import BookService
from src.schemas import BookCreate, BookUpdate, BookResponse, BookListResponse

router = APIRouter(prefix="/books", tags=["books"])


async def get_book_service(session: AsyncSession = Depends(create_database_session)) -> BookService:
    return BookService(session)


@router.get("/", response_model=BookListResponse)
async def get_books(
    page: int = Query(1, ge=1, description="Số trang"),
    size: int = Query(10, ge=1, le=100, description="Số lượng item mỗi trang"),
    book_service: BookService = Depends(get_book_service)
):
    """Lấy danh sách tất cả sách"""
    skip = (page - 1) * size
    books, total = await book_service.get_all_books(skip=skip, limit=size)
    
    return BookListResponse(
        books=[BookResponse.model_validate(book) for book in books],
        total=total,
        page=page,
        size=size
    )


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: str,
    book_service: BookService = Depends(get_book_service)
):
    """Lấy thông tin chi tiết một sách"""
    book = await book_service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Sách với ID {book_id} không tồn tại")
    
    return BookResponse.model_validate(book)


@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    book_data: BookCreate,
    book_service: BookService = Depends(get_book_service)
):
    """Thêm sách mới"""
    try:
        book = await book_service.create_book(book_data)
        return BookResponse.model_validate(book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: str,
    book_data: BookUpdate,
    book_service: BookService = Depends(get_book_service)
):
    """Cập nhật thông tin sách"""
    book = await book_service.update_book(book_id, book_data)
    if not book:
        raise HTTPException(status_code=404, detail=f"Sách với ID {book_id} không tồn tại")
    
    return BookResponse.model_validate(book)


@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: str,
    book_service: BookService = Depends(get_book_service)
):
    """Xóa sách"""
    success = await book_service.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Sách với ID {book_id} không tồn tại") 