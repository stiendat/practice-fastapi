from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.utils.db_utils import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    # Relationship: One user can rent multiple books
    rented_books = relationship("Book", back_populates="rented_by")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    public_date = Column(Date, nullable=False)
    
    # Foreign key to User - nullable because book might not be rented
    rented_by_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    # Relationship: One book can be rented by only one user
    rented_by = relationship("User", back_populates="rented_books")
    
    def __repr__(self):
        return f"<Book(id={self.id}, name='{self.name}', author='{self.author}')>"