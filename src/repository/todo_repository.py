# src/repositories/base.py
from typing import Type, TypeVar, Generic, Optional, List, Any, Dict
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from src.dto.todoDTO import TodoDTO, TodoCreateDTO, TodoUpdateDTO
from src.models.todo import TodoModel
from src.repository.base_repository import BaseRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class TodoRepository(BaseRepository[TodoModel, TodoCreateDTO, TodoUpdateDTO, TodoDTO]):
    def __init__(self):
        super().__init__(TodoModel)

    async def get_by_title(self, db: AsyncSession, *, title: str) -> Optional[TodoDTO]:
        result = await db.execute(select(self.model).where(self.model.title == title))
        return result.scalars().first()
    
    async def update_by_title(
        self, 
        db: AsyncSession, 
        *, 
        obj_in: TodoUpdateDTO | Dict[str, Any]
    ) -> Optional[TodoDTO]:
        # Extract title from the input data
        obj_data = obj_in.dict(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in
        title = obj_data.get("title")
        if not title:
            return None
            
        result = await db.execute(select(self.model).where(self.model.title == title))
        db_obj = result.scalars().first()
        if not db_obj:
            return None
            
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
            
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj