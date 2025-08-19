from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from src.models.todo import TodoStorage
from .schemas import (
    TodoCreate, 
    TodoUpdate, 
    TodoCreateResponse, 
    TodoListResponse, 
    TodoUpdateResponse, 
    TodoDeleteResponse
)

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoCreateResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo_data: TodoCreate):
    """Create a new todo"""
    todo = TodoStorage.create(title=todo_data.title)
    return todo.to_create_response()


@router.get("/", response_model=List[TodoListResponse])
def get_todos():
    """Get all todos"""
    todos = TodoStorage.get_all()
    return [todo.to_dict() for todo in todos]


@router.put("/{todo_id}", response_model=TodoUpdateResponse)
def update_todo(todo_id: str, todo_data: TodoUpdate):
    """Update a todo by ID"""
    # Validate that at least one field is provided
    if todo_data.title is None and todo_data.completed is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one field (title or completed) must be provided"
        )
    
    # Update the todo
    updated_todo = TodoStorage.update(
        todo_id=todo_id,
        title=todo_data.title,
        completed=todo_data.completed
    )
    
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return updated_todo.to_update_response()


@router.delete("/{todo_id}", response_model=TodoDeleteResponse)
def delete_todo(todo_id: str):
    """Delete a todo by ID"""
    success = TodoStorage.delete(todo_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return {"message": "Todo deleted successfully"}
