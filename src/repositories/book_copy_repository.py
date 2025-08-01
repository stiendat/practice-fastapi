from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.models.book_copy import BookCopy, BookCopyStatus
from src.models.book import Book
from src.schemas.book_copy import BookCopyCreate, BookCopyResponse
from .base import BaseRepository

class BookCopyRepository(BaseRepository[BookCopy, BookCopyCreate, BookCopyCreate]):
    def __init__(self, db: Session):
        super().__init__(BookCopy, db)

    def get_copies_by_book_id(self, book_id: int) -> List[BookCopy]:
        """Get all copies of a specific book"""
        return self.db.query(BookCopy).filter(BookCopy.book_id == book_id).all()

    def get_copies_by_status(self, status: BookCopyStatus, skip: int = 0, limit: int = 100) -> List[BookCopy]:
        """Get copies by status"""
        return self.db.query(BookCopy).filter(
            BookCopy.status == status
        ).offset(skip).limit(limit).all()

    def get_available_copies_by_book_id(self, book_id: int) -> List[BookCopy]:
        """Get available copies of a specific book"""
        return self.db.query(BookCopy).filter(
            and_(
                BookCopy.book_id == book_id,
                BookCopy.status == BookCopyStatus.AVAILABLE
            )
        ).all()

    def search_copies(
        self, 
        book_id: Optional[int] = None,
        status: Optional[BookCopyStatus] = None,
        book_title: Optional[str] = None,
        book_author: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[BookCopy]:
        """Search book copies with various filters"""
        query = self.db.query(BookCopy)
        
        if book_id:
            query = query.filter(BookCopy.book_id == book_id)
        
        if status:
            query = query.filter(BookCopy.status == status)
        
        # Join with Book table for title/author search
        if book_title or book_author:
            query = query.join(Book)
            if book_title:
                query = query.filter(Book.title.ilike(f"%{book_title}%"))
            if book_author:
                query = query.filter(Book.author.ilike(f"%{book_author}%"))
        
        return query.offset(skip).limit(limit).all()

    def update_status(self, copy_id: int, new_status: BookCopyStatus) -> Optional[BookCopy]:
        """Update the status of a book copy"""
        copy = self.get(copy_id)
        if copy:
            copy.status = new_status
            self.db.commit()
            self.db.refresh(copy)
        return copy

    def count_by_book_and_status(self, book_id: int, status: BookCopyStatus) -> int:
        """Count copies of a book by status"""
        return self.db.query(BookCopy).filter(
            and_(
                BookCopy.book_id == book_id,
                BookCopy.status == status
            )
        ).count()
