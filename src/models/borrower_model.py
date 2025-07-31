from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.utils.db_utils import Base

class Borrower(Base):
    __tablename__ = "borrowers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String)

    # Relationship to borrowing records
    borrowings = relationship("Borrowing", back_populates="borrower")

    def __repr__(self):
        return f"<Borrower(id={self.id}, name='{self.full_name}', email='{self.email}')>"
