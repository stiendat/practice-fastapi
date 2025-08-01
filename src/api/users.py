from typing import List
from fastapi import APIRouter, Depends, HTTPException

from src.schemas.user import UserCreate, UserResponse, UserUpdate
from src.repositories.user_repository import UserRepository
from src.dependencies import get_user_repository

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, user_repo: UserRepository = Depends(get_user_repository)):
    """Get all users with pagination"""
    users = user_repo.get_all(skip=skip, limit=limit)
    return users

@router.get("/search", response_model=List[UserResponse])
def search_users(
    name: str = None,
    email: str = None,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """Search users by name or email"""
    users = user_repo.search_users(name=name, email=email)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, user_repo: UserRepository = Depends(get_user_repository)):
    """Get a specific user"""
    user = user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, user_repo: UserRepository = Depends(get_user_repository)):
    """Create a new user"""
    # Check if email already exists
    existing_user = user_repo.get_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    return user_repo.create(user)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, user_repo: UserRepository = Depends(get_user_repository)):
    """Update a user"""
    db_user = user_repo.get(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check email uniqueness if email is being updated
    if user.email and user.email != db_user.email:
        existing_user = user_repo.get_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
    
    return user_repo.update(db_user, user)

@router.delete("/{user_id}")
def delete_user(user_id: int, user_repo: UserRepository = Depends(get_user_repository)):
    """Delete a user"""
    user = user_repo.delete(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}
