from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from src.models import Book
from src.schemas.book import BookCreate, BookUpdate


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_books(self, skip: int = 0, limit: int = 100) -> tuple[List[Book], int]:
        """Lấy danh sách tất cả sách với pagination"""
        # Count total
        count_query = select(Book)
        count_result = await self.session.execute(count_query)
        total = len(count_result.scalars().all())

        # Get books with pagination
        query = select(Book).offset(skip).limit(limit)
        result = await self.session.execute(query)
        books = result.scalars().all()
        
        return books, total

    async def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Lấy thông tin chi tiết một sách theo ID"""
        query = select(Book).where(Book.id == book_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_book(self, book_data: BookCreate) -> Book:
        """Tạo sách mới"""
        book = Book(**book_data.model_dump())
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def update_book(self, book_id: str, book_data: BookUpdate) -> Optional[Book]:
        """Cập nhật thông tin sách"""
        # Get existing book
        book = await self.get_book_by_id(book_id)
        if not book:
            return None

        # Update fields
        update_data = book_data.model_dump(exclude_unset=True)
        if update_data:
            query = update(Book).where(Book.id == book_id).values(**update_data)
            await self.session.execute(query)
            await self.session.commit()
            await self.session.refresh(book)

        return book

    async def delete_book(self, book_id: str) -> bool:
        """Xóa sách"""
        book = await self.get_book_by_id(book_id)
        if not book:
            return False

        query = delete(Book).where(Book.id == book_id)
        await self.session.execute(query)
        await self.session.commit()
        return True

    async def update_book_quantity(self, book_id: str, quantity_change: int) -> bool:
        """Cập nhật số lượng sách (dùng cho mượn/trả)"""
        query = update(Book).where(Book.id == book_id).values(
            quantity=Book.quantity + quantity_change
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    async def check_book_availability(self, book_id: str) -> bool:
        """Kiểm tra sách có sẵn để mượn không"""
        book = await self.get_book_by_id(book_id)
        return book is not None and book.quantity > 0 