from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.database import Base
user = relationship("User", back_populates="rentals")

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    returned_at = Column(DateTime, nullable=True)

    # Quan hệ ORM
    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")
