from sqlalchemy import Column, UUID, String, Integer
from sqlalchemy.orm import relationship

from src.utils.db_utils import Base
from src.models.TimestampMixin import TimestampMixin
import uuid

class BookModel(Base, TimestampMixin):
    __tablename__ = "books"

    id: Column = Column(UUID, primary_key=True, default=uuid.uuid4)
    ISBN: Column = Column(String)
    book_title: Column = Column(String, nullable=False)
    book_author: Column = Column(String)
    year_of_publication: Column = Column(Integer)
    total_quantity: Column = Column(Integer)
    available_quantity: Column = Column(Integer)
    publisher: Column = Column(String)
    image_url_s: Column = Column(String)
    image_url_L: Column = Column(String)

    # Relationships
    borrowings = relationship("BorrowingModel", back_populates="book")

    def __repr__(self):
        return f"<BookModel(id={self.id}, name={self.book_title})>"
