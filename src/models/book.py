from sqlalchemy import Column, String, Integer, UUID as SQLAlchemyUUID
from sqlalchemy.dialects.postgresql import UUID
import uuid

from src.utils.db_utils import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    isbn = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year_of_publication = Column(Integer, nullable=True)
    publisher = Column(String, nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    image_url_s = Column(String, nullable=True)  # Small image URL
    image_url_m = Column(String, nullable=True)  # Medium image URL
    image_url_l = Column(String, nullable=True)  # Large image URL

    def __repr__(self):
        return f"<Book(id={self.id}, isbn={self.isbn}, title={self.title}, author={self.author})>"

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            "id": str(self.id),
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "year_of_publication": self.year_of_publication,
            "publisher": self.publisher,
            "quantity": self.quantity,
            "image_url_s": self.image_url_s,
            "image_url_m": self.image_url_m,
            "image_url_l": self.image_url_l,
        }
