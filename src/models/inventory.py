from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.utils.db_utils import Base

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, unique=True)
    total_copies = Column(Integer, default=0, nullable=False)
    available_copies = Column(Integer, default=0, nullable=False)
    borrowed_copies = Column(Integer, default=0, nullable=False)
    lost_copies = Column(Integer, default=0, nullable=False)
    damaged_copies = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    book = relationship("Book", backref="inventory")
    
    def __repr__(self):
        return f"<Inventory(book_id={self.book_id}, total={self.total_copies}, available={self.available_copies})>"
