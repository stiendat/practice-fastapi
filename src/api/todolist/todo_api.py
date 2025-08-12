from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from src.utils.db_utils import create_database_session
from src.dto.todoDTO import TodoCreateDTO, TodoUpdateDTO, TodoDTO
from src.repository.todo_repository import TodoRepository

router = APIRouter(prefix="/todos")

async def get_todo_repo(db: AsyncSession = Depends(create_database_session)) -> TodoRepository:
    return TodoRepository()

@router.get("/", response_model=List[TodoDTO], summary="List all Todos")
async def list_Todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000), 
    repo: TodoRepository = Depends(get_todo_repo),
    db: AsyncSession = Depends(create_database_session)
):
    todos = await repo.get_multi(db, skip=skip, limit=limit)
    if not todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Todos found")
    return todos

@router.get("/", response_model=List[TodoDTO], summary="List all Todos")
async def list_Todos(
    repo: TodoRepository = Depends(get_todo_repo),
    db: AsyncSession = Depends(create_database_session)
):
    todos = await repo.get_all(db)
    if not todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Todos found")
    return todos

@router.get("/num/{todo_id}", response_model=TodoDTO, summary="Get Todo by ID")
async def get_Todo(
    todo_id: UUID,
    repo: TodoRepository = Depends(get_todo_repo),
    db: AsyncSession = Depends(create_database_session)
):
    todo = await repo.get(db, id=todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@router.post("/", response_model=TodoDTO, status_code=status.HTTP_201_CREATED, summary="Create a new Todo")
async def create_Todo(
    todo: TodoCreateDTO,
    repo: TodoRepository = Depends(get_todo_repo),
    db: AsyncSession = Depends(create_database_session)
):
    try:
        created_todo = await repo.create(db, obj_in=todo)
        return created_todo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

@router.put("/{todo_id}", response_model=TodoDTO, summary="Update a Todo")
async def update_Todo(
    todo_id: UUID,
    todo_data: TodoUpdateDTO,
    repo: TodoRepository = Depends(get_todo_repo),
    db: AsyncSession = Depends(create_database_session),
):
    todo = await repo.get(db, id=todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    todo = await repo.update(db, id=todo_id, obj_in=todo_data)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or update failed"
        )
    return todo

@router.put("/", response_model=TodoDTO, summary="Update a Todo")
async def update_Todo(
    todo_data: TodoUpdateDTO,
    repo: TodoRepository = Depends(get_todo_repo),
    db: AsyncSession = Depends(create_database_session)
):
    todo = await repo.update_by_title(db, obj_in=todo_data)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or update failed"
        )
    return todo

@router.delete("/{todo_id}", response_model=dict, summary="Delete a Todo")
async def delete_Todo(
    todo_id: UUID,
    repo: TodoRepository = Depends(get_todo_repo),
    db: AsyncSession = Depends(create_database_session)
) -> dict:
    todo = await repo.get(db, id=todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    success = await repo.delete(db, id=todo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or deletion failed"
        )
    return {"message": "Todo deleted successfully"}