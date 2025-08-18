from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.models import Rental, RentalStatus, Book, User
from src.schemas.rental import RentalCreate, RentalReturn
from src.utils.helpers import generate_uuid


class RentalService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_rentals(self, skip: int = 0, limit: int = 100) -> tuple[List[Rental], int]:
        """Lấy danh sách tất cả lần mượn với pagination"""
        # Count total
        count_query = select(Rental)
        count_result = await self.session.execute(count_query)
        total = len(count_result.scalars().all())

        # Get rentals with pagination and relationships
        query = select(Rental).options(
            selectinload(Rental.user),
            selectinload(Rental.book)
        ).offset(skip).limit(limit)
        result = await self.session.execute(query)
        rentals = result.scalars().all()
        
        return rentals, total

    async def get_rental_by_id(self, rental_id: str) -> Optional[Rental]:
        """Lấy thông tin chi tiết một lần mượn theo ID"""
        query = select(Rental).options(
            selectinload(Rental.user),
            selectinload(Rental.book)
        ).where(Rental.id == rental_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_active_rental_by_book(self, book_id: str) -> Optional[Rental]:
        """Lấy lần mượn đang hoạt động của một sách"""
        query = select(Rental).where(
            Rental.book_id == book_id,
            Rental.status == RentalStatus.BORROWED
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_rental(self, rental_data: RentalCreate) -> Rental:
        """Tạo lần mượn sách mới"""
        # Check if book exists and is available
        book_query = select(Book).where(Book.id == rental_data.book_id)
        book_result = await self.session.execute(book_query)
        book = book_result.scalar_one_or_none()
        
        if not book:
            raise ValueError(f"Sách với ID {rental_data.book_id} không tồn tại")
        
        if book.quantity <= 0:
            raise ValueError(f"Sách {book.title} hiện không có sẵn để mượn")

        # Check if user exists
        user_query = select(User).where(User.id == rental_data.user_id)
        user_result = await self.session.execute(user_query)
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise ValueError(f"Người dùng với ID {rental_data.user_id} không tồn tại")

        # Check if book is already borrowed
        existing_rental = await self.get_active_rental_by_book(rental_data.book_id)
        if existing_rental:
            raise ValueError(f"Sách {book.title} đã được mượn bởi người khác")

        # Create rental
        rental = Rental(
            id=generate_uuid(),
            user_id=rental_data.user_id,
            book_id=rental_data.book_id,
            borrow_date=datetime.now(),
            expected_return_date=rental_data.expected_return_date,
            status=RentalStatus.BORROWED
        )
        self.session.add(rental)

        # Update book quantity
        book.quantity -= 1

        await self.session.commit()
        await self.session.refresh(rental)
        return rental

    async def return_book(self, return_data: RentalReturn) -> Rental:
        """Ghi nhận trả sách"""
        rental = None
        
        if return_data.rental_id:
            # Return by rental ID
            rental = await self.get_rental_by_id(return_data.rental_id)
            if not rental:
                raise ValueError(f"Lần mượn với ID {return_data.rental_id} không tồn tại")
        elif return_data.book_id:
            # Return by book ID
            rental = await self.get_active_rental_by_book(return_data.book_id)
            if not rental:
                raise ValueError(f"Không tìm thấy lần mượn đang hoạt động cho sách {return_data.book_id}")
        else:
            raise ValueError("Cần cung cấp rental_id hoặc book_id")

        if rental.status == RentalStatus.RETURNED:
            raise ValueError("Sách đã được trả trước đó")

        # Update rental status
        rental.actual_return_date = datetime.now()
        rental.status = RentalStatus.RETURNED

        # Update book quantity
        book_query = select(Book).where(Book.id == rental.book_id)
        book_result = await self.session.execute(book_query)
        book = book_result.scalar_one_or_none()
        if book:
            book.quantity += 1

        await self.session.commit()
        await self.session.refresh(rental)
        return rental

    async def get_user_rentals(self, user_id: str) -> List[Rental]:
        """Lấy danh sách lần mượn của một người dùng"""
        query = select(Rental).options(
            selectinload(Rental.book)
        ).where(Rental.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_overdue_rentals(self) -> List[Rental]:
        """Lấy danh sách sách quá hạn"""
        query = select(Rental).options(
            selectinload(Rental.user),
            selectinload(Rental.book)
        ).where(
            Rental.status == RentalStatus.BORROWED,
            Rental.expected_return_date < datetime.now()
        )
        result = await self.session.execute(query)
        return result.scalars().all() 