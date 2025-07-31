from typing import Any

from src.models.borrowing_models import BorrowingModel
from src.dto.borrow_dto import BorrowingCreateDTO, BorrowingUpdateDTO
from src.repository.base_repository import BaseRepository, CreateSchemaType, ModelType
from src.repository.book_repository import book_repository
from src.repository.user_repository import user_repository
from src.utils.db_utils import db_session_context
from sqlalchemy import select
from datetime import datetime

from fastapi import HTTPException


import logging
logger = logging.getLogger(__name__)

class BorrowRepository(BaseRepository[BorrowingModel, BorrowingCreateDTO, BorrowingUpdateDTO]):
    def __init__(self):
        super().__init__(BorrowingModel)
        logger.debug("BorrowRepository initialized")

    async def create(self, obj_in: BorrowingCreateDTO) -> BorrowingModel:
        """
        Create a new borrowing record in the database.
        """
        book = await book_repository.get_by_id(obj_in.book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        if book.available_quantity <= 0:
            raise HTTPException(status_code=400, detail="No available copies of the book")

        user = await user_repository.get_by_id(obj_in.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not obj_in.borrow_date:
            obj_in.borrow_date = datetime.now()

        db = db_session_context.get()
        obj = self.model(**obj_in.dict())
        db.add(obj)
        book = await db.merge(book)
        book.available_quantity -= 1

        await db.commit()
        await db.refresh(obj)
        await db.refresh(book)
        return obj

    async def get_by_field_date(self, field_name: str, value: Any) -> list[BorrowingModel]:
        """
        Retrieve all records that match a specific date field for the entire day.
        """
        db = db_session_context.get()

        # If value is a string, convert it to datetime
        if isinstance(value, str):
            try:
                # Parse the datetime string
                target_datetime = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                # Try parsing without timezone info
                target_datetime = datetime.fromisoformat(value)
        else:
            target_datetime = value

        # Get the start and end of the day
        start_of_day = target_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = target_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Query for records where the date field is within the day range
        query = select(self.model).where(
            getattr(self.model, field_name) >= start_of_day,
            getattr(self.model, field_name) <= end_of_day
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def return_book(self, borrow_id: int) -> BorrowingModel:
        """
        Mark a book as returned and update the available quantity.
        """
        db = db_session_context.get()
        borrow_record = await self.get_by_id(borrow_id)
        if not borrow_record:
            raise HTTPException(status_code=404, detail="Borrow record not found")

        if borrow_record.return_date:
            raise HTTPException(status_code=400, detail="Book already returned")

        book = await book_repository.get_by_id(borrow_record.book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        book.available_quantity += 1
        db.add(book)

        borrow_record.return_date = datetime.now()
        await db.commit()
        await db.refresh(borrow_record)
        await db.refresh(book)
        return borrow_record



borrow_repository = BorrowRepository()