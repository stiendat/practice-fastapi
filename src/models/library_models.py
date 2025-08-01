from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.utils.db_utils import Base


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    
    rentals = relationship("Rental", back_populates="book")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=True)
    
    rentals = relationship("Rental", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, full_name={self.full_name}, email={self.email})>"


class Rental(Base):
    __tablename__ = "rentals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    rental_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, nullable=False, default=False)
    
    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")
    
    def __repr__(self):
        return f"<Rental(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, is_returned={self.is_returned})>"