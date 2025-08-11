from sqlalchemy import Column, UUID, String, Boolean

from src.utils.db_utils import Base
from src.models.TimestampMixin import TimestampMixin
import uuid

class TodoModel(Base,TimestampMixin):

    __tablename__ = "todo"

    id: Column = Column(UUID, primary_key=True, default=uuid.uuid4)
    title: Column = Column(String, nullable=False)
    completed: Column = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<TodoModel(id={self.id}, title={self.title}, completed={self.completed})>"