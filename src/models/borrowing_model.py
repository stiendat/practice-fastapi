from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.utils.db_utils import Base

class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(Integer, ForeignKey("borrowers.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    expected_return_date = Column(Date)
    actual_return_date = Column(Date, nullable=True)

    # Relationships
    borrower = relationship("Borrower", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")

    def __repr__(self):
        return f"<Borrowing(id={self.id}, borrower_id={self.borrower_id}, book_id={self.book_id})>"
