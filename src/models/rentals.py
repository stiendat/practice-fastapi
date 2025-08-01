from sqlalchemy import Column, Integer, String, Date, ForeignKey, UUID
from sqlalchemy.orm import relationship

from src.utils.db_utils import Base

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    book_id = Column(String, ForeignKey("books.isdn"), nullable=False)
    rental_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date, nullable=True)
    
    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")
    
    def __repr__(self):
        return (f"<Rentals(id={self.id}, user_id={self.user_id}, "
                f"book_id={self.book_id}, rental_date={self.rental_date}, "
                f"due_date={self.due_date}, return_date={self.return_date})>")
    
    