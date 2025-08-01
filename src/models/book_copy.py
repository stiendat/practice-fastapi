from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLEnum, DateTime, func
from sqlalchemy.orm import relationship
from enum import Enum
from src.utils.db_utils import Base

class BookCopyStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    LOST = "lost"
    DAMAGED = "damaged"

class BookCopy(Base):
    __tablename__ = "book_copies"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    status = Column(SQLEnum(BookCopyStatus), default=BookCopyStatus.AVAILABLE, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    book = relationship("Book", backref="copies")
    
    def __repr__(self):
        return f"<BookCopy(id={self.id}, book_id={self.book_id}, status={self.status.value})>"
