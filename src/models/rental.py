from sqlalchemy import Column, String, DateTime, UUID as SQLAlchemyUUID, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid

from src.utils.db_utils import Base


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    rent_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    expected_return_date = Column(DateTime, nullable=False)
    actual_return_date = Column(DateTime, nullable=True)
    status = Column(String, default="rented", nullable=False)  # 'rented' or 'returned'

    # Relationships
    user = relationship("User", back_populates="rentals")
    book = relationship("Book")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set default expected return date to 14 days from rent date
        if not self.expected_return_date and self.rent_date:
            self.expected_return_date = self.rent_date + timedelta(days=14)
        elif not self.expected_return_date:
            self.expected_return_date = datetime.utcnow() + timedelta(days=14)

    def __repr__(self):
        return f"<Rental(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status={self.status})>"

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "book_id": str(self.book_id),
            "rent_date": self.rent_date.isoformat() if self.rent_date else None,
            "expected_return_date": self.expected_return_date.isoformat() if self.expected_return_date else None,
            "actual_return_date": self.actual_return_date.isoformat() if self.actual_return_date else None,
            "status": self.status,
        }
