from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.models.book import Book
from src.models.book_copy import BookCopy
from src.models.inventory import Inventory
from src.schemas.book import BookCreate, BookResponse
from .base import BaseRepository

class BookRepository(BaseRepository[Book, BookCreate, BookCreate]):
    def __init__(self, db: Session):
        super().__init__(Book, db)

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.db.query(Book).filter(Book.ISBN == isbn).first()

    def search_books(self, title: Optional[str] = None, author: Optional[str] = None, isbn: Optional[str] = None) -> List[Book]:
        query = self.db.query(Book)
        
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        if isbn:
            query = query.filter(Book.ISBN.ilike(f"%{isbn}%"))
            
        return query.all()

    def get_available_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        """Get books that have available copies"""
        return self.db.query(Book).join(Inventory).filter(
            Inventory.available_copies > 0
        ).offset(skip).limit(limit).all()

    def get_book_with_inventory(self, book_id: int) -> Optional[Book]:
        """Get book with its inventory information"""
        return self.db.query(Book).filter(Book.id == book_id).first()

    def get_book_by_copy_id(self, book_copy_id: int) -> Optional[Tuple[Book, BookCopy]]:
        """Get book information along with copy details by book_copy_id"""
        result = self.db.query(Book, BookCopy).join(
            BookCopy, Book.id == BookCopy.book_id
        ).filter(BookCopy.id == book_copy_id).first()
        
        return result