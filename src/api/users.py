"""
User management API endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.library_models import get_async_session
from src.schemas.library_schemas import (
    UserResponse, UserCreate, UserUpdate, UsersListResponse,
    APIResponse
)
from src.services.library_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


async def get_db():
    """Dependency to get async database session"""
    async with get_async_session() as db:
        yield db


@router.get("/", response_model=UsersListResponse)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of users to return"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of active users with pagination
    """
    try:
        users = await UserService.get_users(db, skip, limit)
        return UsersListResponse(
            total=len(users),
            users=[UserResponse.model_validate(user) for user in users]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific user by ID
    """
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse.model_validate(user)


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user
    """
    try:
        # Check if user with same email already exists
        existing_user = await UserService.get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail=f"User with email {user.email} already exists"
            )
        
        db_user = await UserService.create_user(db, user)
        return UserResponse.model_validate(db_user)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a user's information
    """
    try:
        # Check if updating email to an existing one
        if user_update.email:
            existing_user = await UserService.get_user_by_email(db, user_update.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"User with email {user_update.email} already exists"
                )
        
        updated_user = await UserService.update_user(db, user_id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse.model_validate(updated_user)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")


@router.delete("/{user_id}", response_model=APIResponse)
async def deactivate_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deactivate a user (soft delete - only if no active rentals exist)
    """
    try:
        success = await UserService.deactivate_user(db, user_id)
        if not success:
            # Check if user exists
            user = await UserService.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot deactivate user with active rentals"
                )
        
        return APIResponse(
            success=True,
            message="User deactivated successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to deactivate user: {str(e)}")


@router.get("/{user_id}/rentals")
async def get_user_rentals(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all rentals for a specific user
    """
    # Check if user exists
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        from src.services.library_service import RentalService
        rentals = await RentalService.get_user_rentals(db, user_id, skip, limit)
        
        from src.schemas.library_schemas import RentalsListResponse, RentalResponse
        return RentalsListResponse(
            total=len(rentals),
            rentals=[RentalResponse.model_validate(rental) for rental in rentals]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user rentals: {str(e)}")
