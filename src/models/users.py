from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.orm import relationship

from src.utils.db_utils import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    
    rentals = relationship("Rental", back_populates="users")

    def __repr__(self):
        return (f"<Users(id={self.id}, full_name={self.full_name}, "
                f"email={self.email}, phone={self.phone})>")
