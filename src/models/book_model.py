from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.utils.db_utils import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year_of_publication = Column(Integer, nullable=False)
    publisher = Column(String, nullable=False)
    img_url_s = Column(String)
    img_url_m = Column(String)
    img_url_l = Column(String)
    total_quantity = Column(Integer, default=0)
    available_quantity = Column(Integer, default=0)

    # Relationship to borrowing records
    borrowings = relationship("Borrowing", back_populates="book")

    def __repr__(self):
        return f"<Book(id={self.id}, isbn='{self.isbn}', title='{self.title}')>"
