from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from src.models.inventory import Inventory
from src.models.book import Book
from src.schemas.inventory import InventoryCreate, InventoryUpdate
from .base import BaseRepository

class InventoryRepository(BaseRepository[Inventory, InventoryCreate, InventoryUpdate]):
    def __init__(self, db: Session):
        super().__init__(Inventory, db)

    def get_by_book_id(self, book_id: int) -> Optional[Inventory]:
        """Get inventory record for a specific book"""
        return self.db.query(Inventory).filter(Inventory.book_id == book_id).first()

    def get_all_with_books(self, skip: int = 0, limit: int = 100) -> List[Inventory]:
        """Get all inventory records with book information"""
        return self.db.query(Inventory).join(Book).offset(skip).limit(limit).all()

    def get_low_stock_books(self, threshold: int = 2) -> List[Inventory]:
        """Get books with available copies below threshold"""
        return self.db.query(Inventory).join(Book).filter(
            Inventory.available_copies <= threshold
        ).all()

    def get_out_of_stock_books(self) -> List[Inventory]:
        """Get books with no available copies"""
        return self.db.query(Inventory).join(Book).filter(
            Inventory.available_copies == 0
        ).all()

    def get_books_with_no_copies(self) -> List[Inventory]:
        """Get books with no total copies"""
        return self.db.query(Inventory).join(Book).filter(
            Inventory.total_copies == 0
        ).all()

    def search_inventory(
        self,
        book_title: Optional[str] = None,
        book_author: Optional[str] = None,
        min_available: Optional[int] = None,
        max_available: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Inventory]:
        """Search inventory with various filters"""
        query = self.db.query(Inventory).join(Book)
        
        if book_title:
            query = query.filter(Book.title.ilike(f"%{book_title}%"))
        if book_author:
            query = query.filter(Book.author.ilike(f"%{book_author}%"))
        if min_available is not None:
            query = query.filter(Inventory.available_copies >= min_available)
        if max_available is not None:
            query = query.filter(Inventory.available_copies <= max_available)
        
        return query.offset(skip).limit(limit).all()

    def get_inventory_stats(self) -> dict:
        """Get overall inventory statistics"""
        # Basic counts
        total_books = self.db.query(Inventory).count()
        
        # Sum of all copy types
        totals = self.db.query(
            func.sum(Inventory.total_copies).label('total_copies'),
            func.sum(Inventory.available_copies).label('available_copies'),
            func.sum(Inventory.borrowed_copies).label('borrowed_copies'),
            func.sum(Inventory.lost_copies).label('lost_copies'),
            func.sum(Inventory.damaged_copies).label('damaged_copies')
        ).first()
        
        # Books with issues
        books_with_no_copies = self.db.query(Inventory).filter(
            Inventory.total_copies == 0
        ).count()
        
        books_out_of_stock = self.db.query(Inventory).filter(
            Inventory.available_copies == 0
        ).count()
        
        # Calculate utilization rate
        total_copies = totals.total_copies or 0
        borrowed_copies = totals.borrowed_copies or 0
        utilization_rate = (borrowed_copies / total_copies * 100) if total_copies > 0 else 0
        
        return {
            "total_books": total_books,
            "total_copies_all_books": total_copies,
            "total_available_all_books": totals.available_copies or 0,
            "total_borrowed_all_books": borrowed_copies,
            "total_lost_all_books": totals.lost_copies or 0,
            "total_damaged_all_books": totals.damaged_copies or 0,
            "books_with_no_copies": books_with_no_copies,
            "books_out_of_stock": books_out_of_stock,
            "utilization_rate": round(utilization_rate, 2)
        }

    def adjust_inventory(
        self, 
        book_id: int, 
        adjustment_type: str, 
        copy_type: str, 
        amount: int
    ) -> Optional[Inventory]:
        """Adjust inventory counts for a book"""
        inventory = self.get_by_book_id(book_id)
        if not inventory:
            return None
        
        current_value = getattr(inventory, copy_type)
        
        if adjustment_type == "add":
            new_value = current_value + amount
        elif adjustment_type == "remove":
            new_value = max(0, current_value - amount)  # Don't allow negative
        elif adjustment_type == "set":
            new_value = amount
        else:
            return None
        
        setattr(inventory, copy_type, new_value)
        
        # If adjusting total_copies, ensure it's not less than sum of other types
        if copy_type == "total_copies":
            other_copies = (inventory.available_copies + inventory.borrowed_copies + 
                          inventory.lost_copies + inventory.damaged_copies)
            if new_value < other_copies:
                return None  # Invalid adjustment
        
        self.db.commit()
        self.db.refresh(inventory)
        return inventory

    def sync_inventory_with_copies(self, book_id: int) -> Optional[Inventory]:
        """Synchronize inventory counts with actual book copies in database"""
        from src.models.book_copy import BookCopy, BookCopyStatus
        
        inventory = self.get_by_book_id(book_id)
        if not inventory:
            return None
        
        # Count actual copies by status
        status_counts = self.db.query(
            BookCopy.status,
            func.count(BookCopy.id)
        ).filter(
            BookCopy.book_id == book_id
        ).group_by(BookCopy.status).all()
        
        # Initialize counts
        available = borrowed = lost = damaged = 0
        
        # Map status counts
        for status, count in status_counts:
            if status == BookCopyStatus.AVAILABLE:
                available = count
            elif status == BookCopyStatus.BORROWED:
                borrowed = count
            elif status == BookCopyStatus.LOST:
                lost = count
            elif status == BookCopyStatus.DAMAGED:
                damaged = count
        
        # Update inventory
        inventory.available_copies = available
        inventory.borrowed_copies = borrowed
        inventory.lost_copies = lost
        inventory.damaged_copies = damaged
        inventory.total_copies = available + borrowed + lost + damaged
        
        self.db.commit()
        self.db.refresh(inventory)
        return inventory

    def get_top_borrowed_books(self, limit: int = 10) -> List[Inventory]:
        """Get books with highest number of borrowed copies"""
        return self.db.query(Inventory).join(Book).order_by(
            desc(Inventory.borrowed_copies)
        ).limit(limit).all()

    def get_most_available_books(self, limit: int = 10) -> List[Inventory]:
        """Get books with most available copies"""
        return self.db.query(Inventory).join(Book).order_by(
            desc(Inventory.available_copies)
        ).limit(limit).all()
