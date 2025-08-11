from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession

from src.utils.db_utils import create_database_session, db_session_context
from src.dto import todo_dto
from src.repository.todo_repository import todo_repository

import logging
import uuid

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/todos", tags=["Todo"])

@router.get("", response_model=list[todo_dto.TodoDTO])
async def get_all_todos(db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await todo_repository.get_all()
    if not res:
        logger.warning("No todos found.")
        raise HTTPException(status_code=404, detail="No todos found.")
    logger.info("Retrieved all todos successfully.")
    return res

@router.get("/{id}", response_model=todo_dto.TodoDTO)
async def get_todo_by_id(id: uuid.UUID, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await todo_repository.get_by_id(id)
    if not res:
        logger.error(f"Todo with id {id} not found.")
        raise HTTPException(status_code=404, detail="Todo not found.")
    logger.info(f"Retrieved todo with id {id} successfully.")
    return res

@router.post("", response_model=todo_dto.TodoDTO)
async def create_todo(todo: todo_dto.TodoCreateDTO, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    try:
        res = await todo_repository.create(todo)
        if not res:
            logger.error("Failed to create todo.")
            raise HTTPException(status_code=500, detail="Failed to create todo.")
        logger.info(f"Created todo with id {res.id} successfully.")
        return res
    except Exception as e:
        logger.error(f"Error creating todo: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while creating todo.")

@router.put("/{id}", response_model=todo_dto.TodoDTO)
async def update_todo(id: uuid.UUID, todo: todo_dto.TodoUpdateDTO, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await todo_repository.update(id, todo)
    if not res:
        logger.error(f"Failed to update todo with id {id}.")
        raise HTTPException(status_code=404, detail="Todo not found")  # Remove the period
    logger.info(f"Updated todo with id {id} successfully.")
    return res

@router.delete("/{id}")
async def delete_todo(id: uuid.UUID, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await todo_repository.delete(id)
    if not res:
        logger.error(f"Failed to delete todo with id {id}.")
        raise HTTPException(status_code=404, detail="Todo not found")
    logger.info(f"Deleted todo with id {id} successfully.")
    return {"message": "Todo deleted successfully"}

