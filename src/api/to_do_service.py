from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import uuid
from datetime import datetime

from ..schemas.to_do_schema import TodoCreate, TodoResponse, TodoUpdate, TodoUpdateResponse
from ..models.to_do_models import Todo
from ..utils.db_utils import get_db

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

@router.post("", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(
        id=str(uuid.uuid4()),
        title=todo.title,
        completed=todo.completed,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@router.put("/{id}", response_model=TodoUpdateResponse)
def update_todo(id: UUID, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == str(id)).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.title = todo_update.title
    db_todo.completed = todo_update.completed
    db_todo.updated_at = datetime.now()

    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{id}")
def delete_todo(id: UUID, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == str(id)).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
