from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload

from src.models.library_models import User, Book, Rental, RentalStatus
from src.schemas.library_schemas import (
    UserCreate, UserUpdate, BookCreate, BookUpdate, 
    RentalCreate, ReturnBookRequest
)


class UserService:
    @staticmethod
    async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        query = select(User).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """Create new user"""
        db_user = User(**user_data.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def update_user(db: AsyncSession, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        db_user = await UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db_user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
        """Delete user"""
        db_user = await UserService.get_user_by_id(db, user_id)
        if not db_user:
            return False
        
        await db.delete(db_user)
        await db.commit()
        return True


class BookService:
    @staticmethod
    async def get_all_books(db: AsyncSession, skip: int = 0, limit: int = 100, 
                           available_only: bool = False) -> List[Book]:
        """Get all books with pagination and filtering"""
        query = select(Book)
        
        if available_only:
            query = query.where(Book.is_available == True)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_book_by_id(db: AsyncSession, book_id: UUID) -> Optional[Book]:
        """Get book by ID"""
        query = select(Book).where(Book.id == book_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_book_by_isbn(db: AsyncSession, isbn: str) -> Optional[Book]:
        """Get book by ISBN"""
        query = select(Book).where(Book.isbn == isbn)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def search_books(db: AsyncSession, search_term: str, skip: int = 0, limit: int = 100) -> List[Book]:
        """Search books by title, author or publisher"""
        query = select(Book).where(
            or_(
                Book.title.icontains(search_term),
                Book.author.icontains(search_term),
                Book.publisher.icontains(search_term)
            )
        ).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def create_book(db: AsyncSession, book_data: BookCreate) -> Book:
        """Create new book"""
        db_book = Book(**book_data.model_dump())
        db.add(db_book)
        await db.commit()
        await db.refresh(db_book)
        return db_book
    
    @staticmethod
    async def update_book(db: AsyncSession, book_id: UUID, book_data: BookUpdate) -> Optional[Book]:
        """Update book"""
        db_book = await BookService.get_book_by_id(db, book_id)
        if not db_book:
            return None
        
        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)
        
        db_book.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_book)
        return db_book
    
    @staticmethod
    async def delete_book(db: AsyncSession, book_id: UUID) -> bool:
        """Delete book"""
        db_book = await BookService.get_book_by_id(db, book_id)
        if not db_book:
            return False
        
        await db.delete(db_book)
        await db.commit()
        return True


class RentalService:
    @staticmethod
    async def get_all_rentals(db: AsyncSession, skip: int = 0, limit: int = 100,
                             include_relations: bool = True) -> List[Rental]:
        """Get all rentals with pagination"""
        query = select(Rental)
        
        if include_relations:
            query = query.options(selectinload(Rental.user), selectinload(Rental.book))
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_rental_by_id(db: AsyncSession, rental_id: UUID) -> Optional[Rental]:
        """Get rental by ID"""
        query = select(Rental).options(
            selectinload(Rental.user), 
            selectinload(Rental.book)
        ).where(Rental.id == rental_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_active_rental_by_book(db: AsyncSession, book_id: UUID) -> Optional[Rental]:
        """Get active rental for a specific book"""
        query = select(Rental).where(
            and_(
                Rental.book_id == book_id,
                Rental.status == RentalStatus.RENTED
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_rentals(db: AsyncSession, user_id: UUID, active_only: bool = False) -> List[Rental]:
        """Get rentals for a specific user"""
        query = select(Rental).options(selectinload(Rental.book)).where(Rental.user_id == user_id)
        
        if active_only:
            query = query.where(Rental.status == RentalStatus.RENTED)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def create_rental(db: AsyncSession, rental_data: RentalCreate) -> Optional[Rental]:
        """Create new rental"""
        # Check if book exists and is available
        book = await BookService.get_book_by_id(db, rental_data.book_id)
        if not book or not book.is_available:
            return None
        
        # Check if user exists
        user = await UserService.get_user_by_id(db, rental_data.user_id)
        if not user:
            return None
        
        # Calculate due date
        due_date = datetime.utcnow() + timedelta(days=rental_data.days_to_return)
        
        # Create rental
        db_rental = Rental(
            user_id=rental_data.user_id,
            book_id=rental_data.book_id,
            due_date=due_date,
            status=RentalStatus.RENTED
        )
        
        # Update book availability
        book.is_available = False
        book.updated_at = datetime.utcnow()
        
        db.add(db_rental)
        await db.commit()
        await db.refresh(db_rental)
        
        # Load relationships
        await db.refresh(db_rental, ["user", "book"])
        return db_rental
    
    @staticmethod
    async def return_book(db: AsyncSession, return_data: ReturnBookRequest) -> Optional[Rental]:
        """Return a book"""
        rental = None
        
        if return_data.rental_id:
            rental = await RentalService.get_rental_by_id(db, return_data.rental_id)
        elif return_data.book_id:
            rental = await RentalService.get_active_rental_by_book(db, return_data.book_id)
        
        if not rental or rental.status != RentalStatus.RENTED:
            return None
        
        # Update rental
        rental.return_date = datetime.utcnow()
        rental.status = RentalStatus.RETURNED
        rental.updated_at = datetime.utcnow()
        
        # Update book availability
        book = await BookService.get_book_by_id(db, rental.book_id)
        if book:
            book.is_available = True
            book.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(rental)
        return rental
    
    @staticmethod
    async def get_overdue_rentals(db: AsyncSession) -> List[Rental]:
        """Get all overdue rentals"""
        query = select(Rental).options(
            selectinload(Rental.user),
            selectinload(Rental.book)
        ).where(
            and_(
                Rental.status == RentalStatus.RENTED,
                Rental.due_date < datetime.utcnow()
            )
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def update_overdue_status(db: AsyncSession):
        """Update status of overdue rentals"""
        overdue_rentals = await RentalService.get_overdue_rentals(db)
        
        for rental in overdue_rentals:
            rental.status = RentalStatus.OVERDUE
            rental.updated_at = datetime.utcnow()
        
        if overdue_rentals:
            await db.commit()
        
        return len(overdue_rentals)
