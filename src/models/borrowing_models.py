from sqlalchemy import Column, UUID, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.utils.db_utils import Base
from src.models.TimestampMixin  import TimestampMixin
import uuid

class BorrowingModel(Base, TimestampMixin):
    __tablename__ = "borrowings"

    id: Column = Column(UUID, primary_key=True,default=uuid.uuid4)
    book_id: Column = Column(UUID, ForeignKey("books.id"), nullable=False)
    user_id: Column = Column(UUID, ForeignKey("users.id"), nullable=False)
    borrow_date: Column = Column(DateTime, nullable=False)
    due_date: Column = Column(DateTime, nullable=False)
    return_date: Column = Column(DateTime)

    # Relationships
    book = relationship("BookModel", back_populates="borrowings")
    user = relationship("UserModel", back_populates="borrowings")

    def __repr__(self):
        return f"<BorrowingModel(id={self.id}, name={self.book_title})>"
