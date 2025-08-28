from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from datetime import datetime, timedelta

from src.models.library_models import Book, User, Rental
from src.schemas.library_schemas import BookCreate, BookUpdate, UserCreate, UserUpdate, RentalCreate


class BookService:
    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 10, 
                  search: Optional[str] = None, category: Optional[str] = None) -> List[Book]:
        """Get list of books with optional filtering"""
        query = db.query(Book)
        
        if search:
            search_filter = or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%"),
                Book.isbn.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if category:
            query = query.filter(Book.category.ilike(f"%{category}%"))
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_books_count(db: Session, search: Optional[str] = None, category: Optional[str] = None) -> int:
        """Get total count of books with optional filtering"""
        query = db.query(Book)
        
        if search:
            search_filter = or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%"),
                Book.isbn.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if category:
            query = query.filter(Book.category.ilike(f"%{category}%"))
        
        return query.count()

    @staticmethod
    def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
        """Get book by ID"""
        return db.query(Book).filter(Book.id == book_id).first()

    @staticmethod
    def get_book_by_isbn(db: Session, isbn: str) -> Optional[Book]:
        """Get book by ISBN"""
        return db.query(Book).filter(Book.isbn == isbn).first()

    @staticmethod
    def create_book(db: Session, book: BookCreate) -> Book:
        """Create a new book"""
        db_book = Book(
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            publication_year=book.publication_year,
            publisher=book.publisher,
            category=book.category,
            total_copies=book.total_copies,
            available_copies=book.total_copies,  # Initially all copies are available
            image_url_s=book.image_url_s,
            image_url_m=book.image_url_m,
            image_url_l=book.image_url_l,
            description=book.description
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def update_book(db: Session, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        """Update a book"""
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            return None

        update_data = book_update.model_dump(exclude_unset=True)
        
        # Handle total_copies update
        if "total_copies" in update_data:
            new_total = update_data["total_copies"]
            difference = new_total - db_book.total_copies
            db_book.available_copies = max(0, db_book.available_copies + difference)
            db_book.total_copies = new_total

        # Update other fields
        for field, value in update_data.items():
            if field != "total_copies" and hasattr(db_book, field):
                setattr(db_book, field, value)

        db_book.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def delete_book(db: Session, book_id: int) -> bool:
        """Delete a book"""
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            return False

        # Check if book has active rentals
        active_rentals = db.query(Rental).filter(
            and_(Rental.book_id == book_id, Rental.return_date.is_(None))
        ).first()
        
        if active_rentals:
            return False  # Cannot delete book with active rentals

        db.delete(db_book)
        db.commit()
        return True


class UserService:
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
        """Get list of users"""
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def get_users_count(db: Session) -> int:
        """Get total count of active users"""
        return db.query(User).filter(User.is_active == True).count()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(and_(User.id == user_id, User.is_active == True)).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(and_(User.email == email, User.is_active == True)).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """Create a new user"""
        db_user = User(
            full_name=user.full_name,
            email=user.email,
            phone_number=user.phone_number,
            address=user.address
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update a user"""
        db_user = db.query(User).filter(and_(User.id == user_id, User.is_active == True)).first()
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_user, field):
                setattr(db_user, field, value)

        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Soft delete a user"""
        db_user = db.query(User).filter(and_(User.id == user_id, User.is_active == True)).first()
        if not db_user:
            return False

        # Check if user has active rentals
        active_rentals = db.query(Rental).filter(
            and_(Rental.user_id == user_id, Rental.return_date.is_(None))
        ).first()
        
        if active_rentals:
            return False  # Cannot delete user with active rentals

        db_user.is_active = False
        db_user.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def get_user_rentals(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[Rental]:
        """Get user's rental history"""
        return db.query(Rental).filter(Rental.user_id == user_id).order_by(desc(Rental.created_at)).offset(skip).limit(limit).all()


class RentalService:
    @staticmethod
    def get_rentals(db: Session, skip: int = 0, limit: int = 10, 
                   user_id: Optional[int] = None, book_id: Optional[int] = None,
                   status: Optional[str] = None) -> List[Rental]:
        """Get list of rentals with optional filtering"""
        query = db.query(Rental)
        
        if user_id:
            query = query.filter(Rental.user_id == user_id)
        
        if book_id:
            query = query.filter(Rental.book_id == book_id)
        
        if status == "active":
            query = query.filter(Rental.return_date.is_(None))
        elif status == "returned":
            query = query.filter(Rental.return_date.isnot(None))
        
        return query.order_by(desc(Rental.created_at)).offset(skip).limit(limit).all()

    @staticmethod
    def get_rentals_count(db: Session, user_id: Optional[int] = None, 
                         book_id: Optional[int] = None, status: Optional[str] = None) -> int:
        """Get total count of rentals with optional filtering"""
        query = db.query(Rental)
        
        if user_id:
            query = query.filter(Rental.user_id == user_id)
        
        if book_id:
            query = query.filter(Rental.book_id == book_id)
        
        if status == "active":
            query = query.filter(Rental.return_date.is_(None))
        elif status == "returned":
            query = query.filter(Rental.return_date.isnot(None))
        
        return query.count()

    @staticmethod
    def get_rental_by_id(db: Session, rental_id: int) -> Optional[Rental]:
        """Get rental by ID"""
        return db.query(Rental).filter(Rental.id == rental_id).first()

    @staticmethod
    def create_rental(db: Session, rental: RentalCreate) -> Optional[Rental]:
        """Create a new rental"""
        # Check if book is available
        book = db.query(Book).filter(Book.id == rental.book_id).first()
        if not book or book.available_copies <= 0:
            return None

        # Check if user exists and is active
        user = db.query(User).filter(and_(User.id == rental.user_id, User.is_active == True)).first()
        if not user:
            return None

        # Create rental
        db_rental = Rental(
            user_id=rental.user_id,
            book_id=rental.book_id,
            due_date=rental.due_date
        )
        
        # Update book availability
        book.available_copies -= 1
        
        db.add(db_rental)
        db.commit()
        db.refresh(db_rental)
        return db_rental

    @staticmethod
    def return_book(db: Session, rental_id: int) -> Optional[Rental]:
        """Return a book"""
        rental = db.query(Rental).filter(Rental.id == rental_id).first()
        if not rental or rental.return_date is not None:
            return None

        # Update rental
        rental.return_date = datetime.utcnow()
        
        # Update book availability
        book = db.query(Book).filter(Book.id == rental.book_id).first()
        if book:
            book.available_copies += 1

        db.commit()
        db.refresh(rental)
        return rental

    @staticmethod
    def get_overdue_rentals(db: Session, skip: int = 0, limit: int = 10) -> List[Rental]:
        """Get overdue rentals"""
        current_date = datetime.utcnow()
        return db.query(Rental).filter(
            and_(
                Rental.return_date.is_(None),
                Rental.due_date < current_date
            )
        ).order_by(Rental.due_date).offset(skip).limit(limit).all()