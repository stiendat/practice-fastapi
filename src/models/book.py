from sqlalchemy import Column, Integer, String, DateTime, func
from src.utils.db_utils import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    ISBN = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publication_year = Column(Integer, nullable=True)
    publisher = Column(String, nullable=True)
    image_url_s = Column(String, nullable=True)  # Small image
    image_url_m = Column(String, nullable=True)  # Medium image  
    image_url_l = Column(String, nullable=True)  # Large image
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"
