from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.database import Base
rentals = relationship("Rental", back_populates="user")
user = relationship("User", back_populates="rentals")
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)

    # Quan hệ 1-n với bảng rentals
    rentals = relationship("Rental", back_populates="user")
