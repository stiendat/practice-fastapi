from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from datetime import datetime

from src.utils.db_utils import create_database_session
from src.models.todo_models import Todo, TodoCreate, TodoUpdate, TodoResponse

router = APIRouter()


@router.post("/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(create_database_session)):
    new_todo = Todo(title=todo.title)
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    return new_todo


@router.get("/todos", response_model=list[TodoResponse])
async def get_todos(db: AsyncSession = Depends(create_database_session)):
    result = await db.execute(select(Todo))
    todos = result.scalars().all()
    return todos


@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: UUID, todo: TodoUpdate, db: AsyncSession = Depends(create_database_session)):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    db_todo = result.scalars().first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.title is not None:
        db_todo.title = todo.title
    if todo.completed is not None:
        db_todo.completed = todo.completed
    db_todo.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(db_todo)
    return db_todo


@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: UUID, db: AsyncSession = Depends(create_database_session)):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    db_todo = result.scalars().first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    await db.delete(db_todo)
    await db.commit()
    return {"message": "Todo deleted successfully"}
