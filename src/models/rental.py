from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from src.utils.db_utils import Base
from src.utils.helpers import generate_uuid, get_default_return_date


class RentalStatus(enum.Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(String(36), primary_key=True)  # UUID as primary key
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    book_id = Column(String(13), ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime(timezone=True), nullable=False)
    expected_return_date = Column(DateTime(timezone=True), nullable=False)
    actual_return_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(RentalStatus), default=RentalStatus.BORROWED, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")

    def __repr__(self):
        return f"<Rental(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status={self.status.value})>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "borrow_date": self.borrow_date.isoformat() if self.borrow_date else None,
            "expected_return_date": self.expected_return_date.isoformat() if self.expected_return_date else None,
            "actual_return_date": self.actual_return_date.isoformat() if self.actual_return_date else None,
            "status": self.status.value if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def is_overdue(self) -> bool:
        """Check if the rental is overdue"""
        if self.status == RentalStatus.RETURNED:
            return False
        return datetime.now() > self.expected_return_date 