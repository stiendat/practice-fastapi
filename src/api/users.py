from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db_utils import create_database_session
from src.services.user_service import UserService
from src.schemas import UserCreate, UserUpdate, UserResponse, UserListResponse

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_service(session: AsyncSession = Depends(create_database_session)) -> UserService:
    return UserService(session)


@router.get("/", response_model=UserListResponse)
async def get_users(
    page: int = Query(1, ge=1, description="Số trang"),
    size: int = Query(10, ge=1, le=100, description="Số lượng item mỗi trang"),
    user_service: UserService = Depends(get_user_service)
):
    """Lấy danh sách tất cả người mượn"""
    skip = (page - 1) * size
    users, total = await user_service.get_all_users(skip=skip, limit=size)
    
    return UserListResponse(
        users=[UserResponse.model_validate(user) for user in users],
        total=total,
        page=page,
        size=size
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Lấy thông tin chi tiết một người mượn"""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Người dùng với ID {user_id} không tồn tại")
    
    return UserResponse.model_validate(user)


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Thêm người mượn mới"""
    try:
        user = await user_service.create_user(user_data)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """Cập nhật thông tin người mượn"""
    try:
        user = await user_service.update_user(user_id, user_data)
        if not user:
            raise HTTPException(status_code=404, detail=f"Người dùng với ID {user_id} không tồn tại")
        
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Xóa người mượn"""
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Người dùng với ID {user_id} không tồn tại") 