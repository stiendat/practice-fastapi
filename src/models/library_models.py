"""
Database models for Library Management System

ERD Design:
1. Books (id, title, author, publication_year, isbn, total_copies, available_copies)
2. Users (id, full_name, email, phone_number, created_at)
3. Rentals (id, user_id, book_id, rent_date, expected_return_date, actual_return_date, status)

Relationships:
- Books: One-to-Many with Rentals
- Users: One-to-Many with Rentals
- Rentals: Many-to-One with Books and Users
"""

from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from src.utils.db_utils import Base


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    isbn = Column(String(20), unique=True, nullable=True, index=True)
    publication_year = Column(Integer, nullable=True)
    publisher = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True, default="General")
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    image_url_s = Column(String(500), nullable=True)  # Small image URL
    image_url_m = Column(String(500), nullable=True)  # Medium image URL
    image_url_l = Column(String(500), nullable=True)  # Large image URL
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rentals = relationship("Rental", back_populates="book")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', isbn='{self.isbn}')>"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rentals = relationship("Rental", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, full_name='{self.full_name}', email='{self.email}')>"


class Rental(Base):
    __tablename__ = "rentals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    rent_date = Column(Date, default=date.today, nullable=False)
    expected_return_date = Column(Date, nullable=False)
    actual_return_date = Column(Date, nullable=True)
    status = Column(String(20), default="rented", nullable=False)  # 'rented', 'returned', 'overdue'
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")
    
    def __repr__(self):
        return f"<Rental(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status='{self.status}')>"

