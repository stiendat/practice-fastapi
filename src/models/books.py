from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.utils.db_utils import Base

class Book(Base):
    __tablename__ = "books"

    # ISBN is the primary key and it's a string, not an auto-incrementing integer.
    isdn = Column(String, primary_key=True, index=True)
    book_title = Column(String, nullable=False, index=True)
    book_author = Column(String, index=True)
    year_of_pub = Column(Integer)
    publisher = Column(String)
    image_url_s = Column(String)
    image_url_m = Column(String)
    image_url_l = Column(String)
    
    # Relationship to rentals
    rentals = relationship("Rental", back_populates="books")

    def __repr__(self):
        return (f"<Books(isdn={self.isdn}, book_title={self.book_title}, "
                f"book_author={self.book_author}, year_of_pub={self.year_of_pub}, "
                f"publisher={self.publisher})>")