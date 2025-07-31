from sqlalchemy import Column, Integer, String
from src.db.database import Base
from sqlalchemy.orm import relationship 
rentals = relationship("Rental", back_populates="book")
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    publisher = Column(String, nullable=True)
    image_url_s = Column(String, nullable=True)
    image_url_m = Column(String, nullable=True)
    image_url_l = Column(String, nullable=True)