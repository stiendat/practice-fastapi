from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.utils.db_utils import Base

class Rental(Base):
    __tablename__ = "rentals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rental_date = Column(DateTime, server_default=func.now())
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="rentals")
    rental_items = relationship("RentalItem", back_populates="rental", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Rental(id={self.id}, user_id={self.user_id}, due_date={self.due_date})>"


class RentalItem(Base):
    __tablename__ = "rental_items"
    
    id = Column(Integer, primary_key=True, index=True)
    rental_id = Column(Integer, ForeignKey("rentals.id"), nullable=False)
    book_copy_id = Column(Integer, ForeignKey("book_copies.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    rental = relationship("Rental", back_populates="rental_items")
    book_copy = relationship("BookCopy", backref="rental_items")
    
    def __repr__(self):
        return f"<RentalItem(id={self.id}, rental_id={self.rental_id}, book_copy_id={self.book_copy_id})>"
