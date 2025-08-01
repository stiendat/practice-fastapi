from datetime import datetime
from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, UUID, String, DateTime, Boolean, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from src.utils.db_utils import Base


class RentalStatus(str, Enum):
    RENTED = "RENTED"
    RETURNED = "RETURNED" 
    OVERDUE = "OVERDUE"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    rentals = relationship("Rental", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"


class Book(Base):
    __tablename__ = "books"

    id = Column(UUID, primary_key=True, default=uuid4)
    title = Column(String(500), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    publication_year = Column(Integer, nullable=True)
    publisher = Column(String(255), nullable=True)
    image_url_s = Column(String(500), nullable=True)
    image_url_m = Column(String(500), nullable=True)
    image_url_l = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    rentals = relationship("Rental", back_populates="book")

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author}, isbn={self.isbn})>"


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    book_id = Column(UUID, ForeignKey("books.id"), nullable=False)
    rent_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=False)
    status = Column(ENUM(RentalStatus), default=RentalStatus.RENTED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")

    def __repr__(self):
        return f"<Rental(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status={self.status})>"
