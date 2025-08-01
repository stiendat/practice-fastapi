import uuid
from sqlalchemy import Column, UUID, String, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.utils.db_utils import Base

#Base = declarative_base()

class BookModel(Base):
    __tablename__ = "book_model"

    id: Column = Column(UUID(as_uuid=True), primary_key=True)
    isbn: Column = Column(String(13), unique=True, nullable=False)
    title: Column = Column(String(255), nullable=False)
    author: Column = Column(String(255), nullable=False)
    published_date: Column = Column(String, nullable=True)
    publisher: Column = Column(String(255), nullable=True)
    version: Column = Column(Integer, nullable=True)
    price: Column = Column(Float, nullable=True)
    description: Column = Column(String, nullable=True)
    created_at: Column = Column(DateTime, nullable=False)
    modified_at: Column = Column(DateTime, nullable=False)

    def __repr__(self):
        return (f"<BookModel(id={self.id}, title={self.title}, author={self.author}, "
                f"published_date={self.published_date}, publisher={self.publisher}, "
                f"version={self.version}, price={self.price}, description={self.description}, "
                f"created_at={self.created_at}, modified_at={self.modified_at})>")

class UserModel(Base):
    __tablename__ = "user_model"

    id: Column = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Column = Column(String(100), nullable=False)
    email: Column = Column(String(100), nullable=False)
    phone: Column = Column(String(100), nullable=False)
    address: Column = Column(String(20), nullable=False)
    created_at: Column = Column(DateTime, nullable=False)
    modified_at: Column = Column(DateTime, nullable=False)

    def __repr__(self):
        return (f"<UserModel(id={self.id}, username={self.username}, email={self.email}, "
                f"phone={self.phone}, address={self.address}, created_at={self.created_at}, "
                f"modified_at={self.modified_at})>")

class BookRentalModel(Base):
    __tablename__ = "book_rental_model"

    id: Column = Column(Integer, primary_key=True)
    book_id: Column = Column(UUID(as_uuid=True), ForeignKey(BookModel.id), nullable=False)
    user_id: Column = Column(UUID(as_uuid=True), ForeignKey(UserModel.id), nullable=False)
    rental_date: Column = Column(DateTime, nullable=False)
    expected_return_date: Column = Column(DateTime, nullable=True)
    volume: Column = Column(Integer, nullable=True)

    book = relationship("BookModel", back_populates="storages")
    user = relationship("UserModel", back_populates="storages")

    def __repr__(self):
        return (f"<BookRentalModel(id={self.id}, book_id={self.book_id}, user_id={self.user_id}, "
                f"rental_date={self.rental_date}, expected_return_date={self.expected_return_date}, volume={self.volume})>")
    
class StorageModel(Base):
    __tablename__ = "storage_model"

    id: Column = Column(Integer, primary_key=True)
    book_id: Column = Column(UUID(as_uuid=True), ForeignKey(BookModel.id), nullable=False)
    total_volume: Column = Column(Integer, nullable=False)
    available_volume: Column = Column(Integer, nullable=False)
    created_at: Column = Column(DateTime, nullable=False, server_default=func.now())
    modified_at: Column = Column(DateTime, nullable=False)

    book = relationship("BookModel", back_populates="storages")

    def __repr__(self):
        return (f"<StorageModel(id={self.id}, book_id={self.book_id}, total_volume={self.total_volume}, "
                f"available_volume={self.available_volume}, created_at={self.created_at}, "
                f"modified_at={self.modified_at})>")