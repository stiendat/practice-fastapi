from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.models.rental import Rental, RentalItem
from src.models.book_copy import BookCopy, BookCopyStatus
from src.models.inventory import Inventory
from src.schemas.rental import RentalCreate
from .base import BaseRepository

class RentalRepository(BaseRepository[Rental, RentalCreate, RentalCreate]):
    def __init__(self, db: Session):
        super().__init__(Rental, db)

    def create_rental(self, user_id: int, book_ids: List[int], due_date: Optional[datetime] = None) -> Rental:
        """
        Create a new rental by borrowing multiple books.
        Finds available copies for each book and creates rental items.
        """
        # Set default due date to 14 days from now
        if due_date is None:
            due_date = datetime.now() + timedelta(days=14)
        
        # Find available copies for each book
        available_copies = []
        for book_id in book_ids:
            # Find an available copy of this book
            copy = self.db.query(BookCopy).filter(
                and_(
                    BookCopy.book_id == book_id,
                    BookCopy.status == BookCopyStatus.AVAILABLE
                )
            ).first()
            
            if not copy:
                raise ValueError(f"No available copies for book ID {book_id}")
            
            available_copies.append(copy)
        
        # Create the rental
        rental = Rental(
            user_id=user_id,
            due_date=due_date,
            rental_date=datetime.now()
        )
        self.db.add(rental)
        self.db.flush()  # Get the rental ID
        
        # Create rental items and update copy status
        for copy in available_copies:
            # Create rental item
            rental_item = RentalItem(
                rental_id=rental.id,
                book_copy_id=copy.id
            )
            self.db.add(rental_item)
            
            # Update copy status to borrowed
            copy.status = BookCopyStatus.BORROWED
            
            # Update inventory counts
            inventory = self.db.query(Inventory).filter(Inventory.book_id == copy.book_id).first()
            if inventory:
                inventory.available_copies -= 1
                inventory.borrowed_copies += 1
        
        self.db.commit()
        self.db.refresh(rental)
        return rental

    def return_rental(self, rental_id: int) -> dict:
        """
        Return all books in a rental.
        """
        rental = self.db.query(Rental).filter(Rental.id == rental_id).first()
        if not rental:
            raise ValueError(f"Rental {rental_id} not found")
        
        if rental.return_date:
            raise ValueError(f"Rental {rental_id} already returned")
        
        returned_copies = []
        
        # Return each book copy in the rental
        for rental_item in rental.rental_items:
            copy = rental_item.book_copy
            
            # Update copy status to available
            copy.status = BookCopyStatus.AVAILABLE
            returned_copies.append(copy.id)
            
            # Update inventory counts
            inventory = self.db.query(Inventory).filter(Inventory.book_id == copy.book_id).first()
            if inventory:
                inventory.available_copies += 1
                inventory.borrowed_copies -= 1
        
        # Mark rental as returned
        rental.return_date = datetime.now()
        
        self.db.commit()
        
        return {
            "rental_id": rental_id,
            "return_date": rental.return_date,
            "returned_copies": returned_copies,
            "message": f"Successfully returned {len(returned_copies)} books"
        }

    def return_book_copies(self, book_copy_ids: List[int]) -> dict:
        """
        Return specific book copies (partial return).
        """
        returned_copies = []
        
        for copy_id in book_copy_ids:
            copy = self.db.query(BookCopy).filter(BookCopy.id == copy_id).first()
            if not copy:
                continue
            
            if copy.status != BookCopyStatus.BORROWED:
                continue
            
            # Find the rental item for this copy
            rental_item = self.db.query(RentalItem).filter(
                RentalItem.book_copy_id == copy_id
            ).join(Rental).filter(Rental.return_date.is_(None)).first()
            
            if not rental_item:
                continue
            
            # Update copy status to available
            copy.status = BookCopyStatus.AVAILABLE
            returned_copies.append(copy_id)
            
            # Update inventory counts
            inventory = self.db.query(Inventory).filter(Inventory.book_id == copy.book_id).first()
            if inventory:
                inventory.available_copies += 1
                inventory.borrowed_copies -= 1
            
            # Check if all items in the rental are returned
            rental = rental_item.rental
            all_returned = all(
                item.book_copy.status != BookCopyStatus.BORROWED 
                for item in rental.rental_items
            )
            
            if all_returned:
                rental.return_date = datetime.now()
        
        self.db.commit()
        
        return {
            "returned_copies": returned_copies,
            "message": f"Successfully returned {len(returned_copies)} books"
        }

    def get_user_rentals(self, user_id: int, include_returned: bool = False) -> List[Rental]:
        """Get all rentals for a specific user"""
        query = self.db.query(Rental).filter(Rental.user_id == user_id)
        
        if not include_returned:
            query = query.filter(Rental.return_date.is_(None))
        
        return query.all()

    def get_overdue_rentals(self) -> List[Rental]:
        """Get all overdue rentals"""
        current_time = datetime.now()
        return self.db.query(Rental).filter(
            and_(
                Rental.due_date < current_time,
                Rental.return_date.is_(None)
            )
        ).all()

    def get_rental_with_items(self, rental_id: int) -> Optional[Rental]:
        """Get rental with all its items loaded"""
        return self.db.query(Rental).filter(Rental.id == rental_id).first()
