from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from src.models.todo import Todo
from src.schemas.todo import TodoCreate, TodoUpdate
from typing import List, Optional
import uuid


class TodoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_todo(self, todo_data: TodoCreate) -> Todo:
        """Create a new todo"""
        todo = Todo(
            title=todo_data.title,
            completed=False
        )
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)
        return todo

    async def get_todos(self) -> List[Todo]:
        """Get all todos"""
        result = await self.db.execute(select(Todo).order_by(Todo.created_at.desc()))
        return result.scalars().all()

    async def get_todo_by_id(self, todo_id: str) -> Optional[Todo]:
        """Get todo by ID"""
        try:
            todo_uuid = uuid.UUID(todo_id)
        except ValueError:
            return None
        
        result = await self.db.execute(select(Todo).where(Todo.id == todo_uuid))
        return result.scalar_one_or_none()

    async def update_todo(self, todo_id: str, todo_data: TodoUpdate) -> Optional[Todo]:
        """Update a todo"""
        todo = await self.get_todo_by_id(todo_id)
        if not todo:
            return None

        update_data = {}
        if todo_data.title is not None:
            update_data["title"] = todo_data.title
        if todo_data.completed is not None:
            update_data["completed"] = todo_data.completed

        if update_data:
            update_data["updated_at"] = todo.updated_at
            await self.db.execute(
                update(Todo)
                .where(Todo.id == todo.id)
                .values(**update_data)
            )
            await self.db.commit()
            await self.db.refresh(todo)

        return todo

    async def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo"""
        todo = await self.get_todo_by_id(todo_id)
        if not todo:
            return False

        await self.db.delete(todo)
        await self.db.commit()
        return True
