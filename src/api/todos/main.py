from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.db_utils import create_database_session
from src.services.todo_service import TodoService
from src.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from typing import List

router = APIRouter()


@router.post("/todos", response_model=TodoResponse, status_code=201)
async def create_todo(
    todo_data: TodoCreate,
    session: AsyncSession = Depends(create_database_session)
):
    """Create a new todo"""
    if not todo_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title cannot be empty"
        )
    
    todo_service = TodoService(session)
    todo = await todo_service.create_todo(todo_data)
    return TodoResponse(
        id=str(todo.id),
        title=todo.title,
        completed=todo.completed,
        created_at=todo.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=todo.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    )


@router.get("/todos", response_model=List[TodoResponse])
async def get_todos(session: AsyncSession = Depends(create_database_session)):
    """Get all todos"""
    todo_service = TodoService(session)
    todos = await todo_service.get_todos()
    return [
        TodoResponse(
            id=str(todo.id),
            title=todo.title,
            completed=todo.completed,
            created_at=todo.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=todo.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        )
        for todo in todos
    ]


@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str,
    session: AsyncSession = Depends(create_database_session)
):
    """Get a specific todo by ID"""
    todo_service = TodoService(session)
    todo = await todo_service.get_todo_by_id(todo_id)
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return TodoResponse(
        id=str(todo.id),
        title=todo.title,
        completed=todo.completed,
        created_at=todo.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=todo.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    )


@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str,
    todo_data: TodoUpdate,
    session: AsyncSession = Depends(create_database_session)
):
    """Update a todo"""
    if not todo_data.title and todo_data.completed is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one field must be provided"
        )
    
    if todo_data.title is not None and not todo_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title cannot be empty"
        )
    
    todo_service = TodoService(session)
    todo = await todo_service.update_todo(todo_id, todo_data)
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return TodoResponse(
        id=str(todo.id),
        title=todo.title,
        completed=todo.completed,
        created_at=todo.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=todo.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    )


@router.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: str,
    session: AsyncSession = Depends(create_database_session)
):
    """Delete a todo"""
    todo_service = TodoService(session)
    success = await todo_service.delete_todo(todo_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return {"message": "Todo deleted successfully"}
