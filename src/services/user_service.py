from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from src.models import User
from src.schemas.user import UserCreate, UserUpdate
from src.utils.helpers import generate_uuid


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> tuple[List[User], int]:
        """Lấy danh sách tất cả người mượn với pagination"""
        # Count total
        count_query = select(User)
        count_result = await self.session.execute(count_query)
        total = len(count_result.scalars().all())

        # Get users with pagination
        query = select(User).offset(skip).limit(limit)
        result = await self.session.execute(query)
        users = result.scalars().all()
        
        return users, total

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Lấy thông tin chi tiết một người mượn theo ID"""
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Lấy người mượn theo email"""
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        """Tạo người mượn mới"""
        # Check if email already exists
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"Email {user_data.email} đã tồn tại")

        user = User(
            id=generate_uuid(),
            **user_data.model_dump()
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Cập nhật thông tin người mượn"""
        # Get existing user
        user = await self.get_user_by_id(user_id)
        if not user:
            return None

        # Check email uniqueness if email is being updated
        if user_data.email and user_data.email != user.email:
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise ValueError(f"Email {user_data.email} đã tồn tại")

        # Update fields
        update_data = user_data.model_dump(exclude_unset=True)
        if update_data:
            query = update(User).where(User.id == user_id).values(**update_data)
            await self.session.execute(query)
            await self.session.commit()
            await self.session.refresh(user)

        return user

    async def delete_user(self, user_id: str) -> bool:
        """Xóa người mượn"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False

        query = delete(User).where(User.id == user_id)
        await self.session.execute(query)
        await self.session.commit()
        return True 