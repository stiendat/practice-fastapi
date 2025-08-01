from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.models.models import BookModel, BookRentalModel, StorageModel
from src.models.schemas import BookCreate, BookRead
from .base import BaseRepository

class BookRepository(BaseRepository[BookModel, BookCreate, BookRead]):
    def __init__(self, db: Session):
        super().__init__(BookModel, db)

    def get_by_id(self, id: str) -> Optional[BookModel]:
        return self.db.query(BookModel).filter(BookModel.id == id).first()

    def search_books(self, title: Optional[str] = None, author: Optional[str] = None, id: Optional[str] = None) -> List[BookModel]:
        query = self.db.query(BookModel)

        if title:
            query = query.filter(BookModel.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(BookModel.author.ilike(f"%{author}%"))
        if id:
            query = query.filter(BookModel.isbn.ilike(f"%{id}%"))

        return query.all()

    def get_available_books(self, skip: int = 0, limit: int = 100) -> List[BookModel]:
        """Get books that have available copies"""
        return self.db.query(BookModel).join(StorageModel).filter(
            StorageModel.available_volume > 0
        ).offset(skip).limit(limit).all()