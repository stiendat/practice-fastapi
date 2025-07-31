import uuid

from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import relationship

from src.utils.db_utils import Base
from src.models.TimestampMixin import TimestampMixin


class UserModel(Base, TimestampMixin):
    __tablename__ = "users"

    id: Column = Column(UUID, primary_key=True, default=uuid.uuid4)
    full_name: Column = Column(String, nullable=False)
    email: Column = Column(String)
    phone_number: Column = Column(String)

    # Relationships
    borrowings = relationship("BorrowingModel", back_populates="user")

    def __repr__(self):
        return f"<UserModel(id={self.id}, name={self.full_name})>"
