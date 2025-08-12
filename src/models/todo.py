from sqlalchemy import Boolean, Column, UUID, DateTime, String, func

from src.utils.db_utils import Base

class TodoModel(Base):
    __tablename__ = "todolist"
    
    created_at: Column = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Column = Column(
        DateTime, 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    id: Column = Column(UUID, primary_key=True)
    title: Column = Column(String, nullable=False)
    completed: Column = Column(Boolean, nullable=False)
    