from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession

from src.utils.db_utils import create_database_session, db_session_context
from src.dto import user_dto
from src.repository.user_repository import user_repository

import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/users/", response_model=user_dto.UserDTO)
async def create_user(user: user_dto.UserCreateDTO, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await user_repository.create(user)
    if not res:
        raise HTTPException(status_code=400, detail="User creation failed")
    return res

@router.get("/all-users/", response_model=list[user_dto.UserDTO])
async def get_all_users(db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await user_repository.get_all()
    if not res:
        raise HTTPException(status_code=404, detail="No users found")
    return res

@router.get("/users/", response_model=list[user_dto.UserDTO])
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    user = await user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/field", response_model=user_dto.UserDTO)
async def get_user_by_field(field_name: str, value: str, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    user = await user_repository.get_by_field(field_name, value)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with {field_name}={value} not found")
    return user

@router.put("/users/{user_id}", response_model=user_dto.UserDTO)
async def update_user(
    user_id: uuid.UUID, user: user_dto.UserUpdateDTO, db: AsyncSession = Depends(create_database_session)
):
    db_session_context.set(db)
    updated_user = await user_repository.update(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return updated_user

@router.delete("/users", response_model=dict)
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    user = await user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user_repository.delete(user_id)
    logger.info(f"User with ID {user_id} deleted successfully")
    return {"detail": "User deleted successfully"}