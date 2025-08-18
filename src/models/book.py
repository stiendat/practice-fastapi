from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.utils.db_utils import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(String(13), primary_key=True)  
    title = Column(String(500), nullable=False)
    author = Column(String(200), nullable=False)
    year_of_publication = Column(Integer, nullable=True)
    publisher = Column(String(200), nullable=True)
    image_url_s = Column(Text, nullable=True)
    image_url_m = Column(Text, nullable=True)
    image_url_l = Column(Text, nullable=True)
    quantity = Column(Integer, default=1, nullable=False) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    rentals = relationship("Rental", back_populates="book")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', quantity={self.quantity})>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year_of_publication": self.year_of_publication,
            "publisher": self.publisher,
            "image_url_s": self.image_url_s,
            "image_url_m": self.image_url_m,
            "image_url_l": self.image_url_l,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 