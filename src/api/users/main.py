from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.utils.db_utils import create_database_session
from src.models.library_models import User
from src.models.schemas import UserResponse, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
async def get_all_users(session: AsyncSession = Depends(create_database_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(create_database_session)):
    result = await session.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user