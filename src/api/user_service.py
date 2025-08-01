from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.models.models import User
from src.schemas.user_schema import UserCreate, UserResponse
from src.utils.db_utils import create_database_session
from src.utils.password_utils import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
async def get_users(
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """
    Get all users from the database
    """
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    """
    Create a new user with hashed password
    """
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create new user with hashed password
    new_user = User(
        email=user.email,
        password=hashed_password
    )
    
    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )