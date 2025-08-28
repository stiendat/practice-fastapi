from datetime import datetime
from typing import Optional
import uuid


class Todo:
    """Todo model for in-memory storage"""

    def __init__(self, title: str, completed: bool = False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.completed = completed
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, title: Optional[str] = None, completed: Optional[bool] = None):
        """Update todo fields and timestamp"""
        if title is not None:
            self.title = title
        if completed is not None:
            self.completed = completed
        self.updated_at = datetime.now()

    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def to_create_response(self):
        """Convert to create response format (without timestamps)"""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed
        }

    def to_update_response(self):
        """Convert to update response format (with updated_at only)"""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }


# In-memory storage
todos_storage = {}


class TodoStorage:
    """Simple in-memory storage for todos"""

    @staticmethod
    def create(title: str) -> Todo:
        """Create a new todo"""
        todo = Todo(title=title)
        todos_storage[todo.id] = todo
        return todo

    @staticmethod
    def get_all() -> list[Todo]:
        """Get all todos"""
        return list(todos_storage.values())

    @staticmethod
    def get_by_id(todo_id: str) -> Optional[Todo]:
        """Get todo by ID"""
        return todos_storage.get(todo_id)

    @staticmethod
    def update(todo_id: str, title: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Todo]:
        """Update todo by ID"""
        todo = todos_storage.get(todo_id)
        if todo:
            todo.update(title=title, completed=completed)
            return todo
        return None

    @staticmethod
    def delete(todo_id: str) -> bool:
        """Delete todo by ID"""
        if todo_id in todos_storage:
            del todos_storage[todo_id]
            return True
        return False