from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.models import UserModel
from src.models.schemas import UserRead, UserCreate
from .base import BaseRepository

class UserRepository(BaseRepository[UserModel, UserCreate, UserRead]):
    def __init__(self, db: Session):
        super().__init__(UserModel, db)

    def get_by_email(self, email: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.email == email).first()
    
    def get_by_phone(self, phone: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.phone == phone).first()

    def search_users(self, 
                     user_id: Optional[str] = None, 
                     name: Optional[str] = None, 
                     email: Optional[str] = None,
                     phone: Optional[str] = None) -> List[UserModel]:
        query = self.db.query(UserModel)
        if user_id:
            query = query.filter(UserModel.user_id == user_id)
        if name:
            query = query.filter(UserModel.name.ilike(f"%{name}%"))
        if email:
            query = query.filter(UserModel.email.ilike(f"%{email}%"))
        if phone:
            query = query.filter(UserModel.phone.ilike(f"%{phone}%"))
        return query.all()
