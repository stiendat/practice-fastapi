from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from src.schemas.inventory import (
    InventoryCreate, InventoryUpdate, InventoryResponse,
    InventoryWithBookResponse, InventoryAdjustment, InventoryStats, LowStockAlert
)
from src.repositories.inventory_repository import InventoryRepository
from src.repositories.book_repository import BookRepository
from src.dependencies import get_inventory_repository, get_book_repository

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/", response_model=List[InventoryResponse])
def get_all_inventory(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Get all inventory records with pagination"""
    inventory = inventory_repo.get_all(skip=skip, limit=limit)
    return inventory

@router.get("/with-books", response_model=List[InventoryWithBookResponse])
def get_inventory_with_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Get all inventory records with book information"""
    inventory = inventory_repo.get_all_with_books(skip=skip, limit=limit)
    
    result = []
    for inv in inventory:
        result.append(InventoryWithBookResponse(
            id=inv.id,
            book_id=inv.book_id,
            total_copies=inv.total_copies,
            available_copies=inv.available_copies,
            borrowed_copies=inv.borrowed_copies,
            lost_copies=inv.lost_copies,
            damaged_copies=inv.damaged_copies,
            created_at=inv.created_at,
            modified_at=inv.modified_at,
            book_title=inv.book.title,
            book_author=inv.book.author,
            book_isbn=inv.book.ISBN,
            book_publisher=inv.book.publisher
        ))
    
    return result

@router.get("/search", response_model=List[InventoryWithBookResponse])
def search_inventory(
    book_title: Optional[str] = Query(None, description="Search by book title"),
    book_author: Optional[str] = Query(None, description="Search by book author"),
    min_available: Optional[int] = Query(None, ge=0, description="Minimum available copies"),
    max_available: Optional[int] = Query(None, ge=0, description="Maximum available copies"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Search inventory with various filters"""
    inventory = inventory_repo.search_inventory(
        book_title=book_title,
        book_author=book_author,
        min_available=min_available,
        max_available=max_available,
        skip=skip,
        limit=limit
    )
    
    result = []
    for inv in inventory:
        result.append(InventoryWithBookResponse(
            id=inv.id,
            book_id=inv.book_id,
            total_copies=inv.total_copies,
            available_copies=inv.available_copies,
            borrowed_copies=inv.borrowed_copies,
            lost_copies=inv.lost_copies,
            damaged_copies=inv.damaged_copies,
            created_at=inv.created_at,
            modified_at=inv.modified_at,
            book_title=inv.book.title,
            book_author=inv.book.author,
            book_isbn=inv.book.ISBN,
            book_publisher=inv.book.publisher
        ))
    
    return result

@router.get("/stats", response_model=InventoryStats)
def get_inventory_stats(
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Get overall inventory statistics"""
    stats = inventory_repo.get_inventory_stats()
    return InventoryStats(**stats)

@router.get("/low-stock", response_model=List[LowStockAlert])
def get_low_stock_books(
    threshold: int = Query(2, ge=0, description="Minimum available copies threshold"),
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Get books with available copies below threshold"""
    low_stock = inventory_repo.get_low_stock_books(threshold=threshold)
    
    alerts = []
    for inv in low_stock:
        alerts.append(LowStockAlert(
            book_id=inv.book_id,
            book_title=inv.book.title,
            book_author=inv.book.author,
            available_copies=inv.available_copies,
            total_copies=inv.total_copies,
            threshold_violated=threshold
        ))
    
    return alerts

@router.get("/out-of-stock", response_model=List[InventoryWithBookResponse])
def get_out_of_stock_books(
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Get books with no available copies"""
    out_of_stock = inventory_repo.get_out_of_stock_books()
    
    result = []
    for inv in out_of_stock:
        result.append(InventoryWithBookResponse(
            id=inv.id,
            book_id=inv.book_id,
            total_copies=inv.total_copies,
            available_copies=inv.available_copies,
            borrowed_copies=inv.borrowed_copies,
            lost_copies=inv.lost_copies,
            damaged_copies=inv.damaged_copies,
            created_at=inv.created_at,
            modified_at=inv.modified_at,
            book_title=inv.book.title,
            book_author=inv.book.author,
            book_isbn=inv.book.ISBN,
            book_publisher=inv.book.publisher
        ))
    
    return result

@router.get("/no-copies", response_model=List[InventoryWithBookResponse])
def get_books_with_no_copies(
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Get books with no total copies"""
    no_copies = inventory_repo.get_books_with_no_copies()
    
    result = []
    for inv in no_copies:
        result.append(InventoryWithBookResponse(
            id=inv.id,
            book_id=inv.book_id,
            total_copies=inv.total_copies,
            available_copies=inv.available_copies,
            borrowed_copies=inv.borrowed_copies,
            lost_copies=inv.lost_copies,
            damaged_copies=inv.damaged_copies,
            created_at=inv.created_at,
            modified_at=inv.modified_at,
            book_title=inv.book.title,
            book_author=inv.book.author,
            book_isbn=inv.book.ISBN,
            book_publisher=inv.book.publisher
        ))
    
    return result

@router.get("/top-borrowed", response_model=List[InventoryWithBookResponse])
def get_top_borrowed_books(
    limit: int = Query(10, ge=1, le=50, description="Number of top books to return"),
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Get books with highest number of borrowed copies"""
    top_borrowed = inventory_repo.get_top_borrowed_books(limit=limit)
    
    result = []
    for inv in top_borrowed:
        result.append(InventoryWithBookResponse(
            id=inv.id,
            book_id=inv.book_id,
            total_copies=inv.total_copies,
            available_copies=inv.available_copies,
            borrowed_copies=inv.borrowed_copies,
            lost_copies=inv.lost_copies,
            damaged_copies=inv.damaged_copies,
            created_at=inv.created_at,
            modified_at=inv.modified_at,
            book_title=inv.book.title,
            book_author=inv.book.author,
            book_isbn=inv.book.ISBN,
            book_publisher=inv.book.publisher
        ))
    
    return result

@router.get("/most-available", response_model=List[InventoryWithBookResponse])
def get_most_available_books(
    limit: int = Query(10, ge=1, le=50, description="Number of books to return"),
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Get books with most available copies"""
    most_available = inventory_repo.get_most_available_books(limit=limit)
    
    result = []
    for inv in most_available:
        result.append(InventoryWithBookResponse(
            id=inv.id,
            book_id=inv.book_id,
            total_copies=inv.total_copies,
            available_copies=inv.available_copies,
            borrowed_copies=inv.borrowed_copies,
            lost_copies=inv.lost_copies,
            damaged_copies=inv.damaged_copies,
            created_at=inv.created_at,
            modified_at=inv.modified_at,
            book_title=inv.book.title,
            book_author=inv.book.author,
            book_isbn=inv.book.ISBN,
            book_publisher=inv.book.publisher
        ))
    
    return result

@router.get("/book/{book_id}", response_model=InventoryResponse)
def get_inventory_by_book_id(
    book_id: int,
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Get inventory record for a specific book"""
    inventory = inventory_repo.get_by_book_id(book_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found for this book")
    return inventory

@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory(
    inventory_id: int,
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Get a specific inventory record by ID"""
    inventory = inventory_repo.get(inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return inventory

@router.post("/", response_model=InventoryResponse, status_code=201)
def create_inventory(
    inventory: InventoryCreate,
    inventory_repo: InventoryRepository = Depends(get_inventory_repository),
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Create a new inventory record"""
    # Verify that the book exists
    book = book_repo.get(inventory.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if inventory already exists for this book
    existing_inventory = inventory_repo.get_by_book_id(inventory.book_id)
    if existing_inventory:
        raise HTTPException(status_code=400, detail="Inventory record already exists for this book")
    
    return inventory_repo.create(inventory)

@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int,
    inventory_update: InventoryUpdate,
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Update an inventory record"""
    db_inventory = inventory_repo.get(inventory_id)
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    
    return inventory_repo.update(db_inventory, inventory_update)

@router.patch("/{inventory_id}/adjust", response_model=InventoryResponse)
def adjust_inventory(
    inventory_id: int,
    adjustment: InventoryAdjustment,
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Adjust inventory counts for a specific record"""
    db_inventory = inventory_repo.get(inventory_id)
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    
    adjusted = inventory_repo.adjust_inventory(
        book_id=db_inventory.book_id,
        adjustment_type=adjustment.adjustment_type,
        copy_type=adjustment.copy_type,
        amount=adjustment.amount
    )
    
    if not adjusted:
        raise HTTPException(status_code=400, detail="Invalid adjustment parameters")
    
    return adjusted

@router.patch("/book/{book_id}/sync", response_model=InventoryResponse)
def sync_inventory_with_copies(
    book_id: int,
    inventory_repo: InventoryRepository = Depends(get_inventory_repository),
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Synchronize inventory counts with actual book copies in database"""
    # Verify book exists
    book = book_repo.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    synced = inventory_repo.sync_inventory_with_copies(book_id)
    if not synced:
        raise HTTPException(status_code=404, detail="Inventory record not found for this book")
    
    return synced

@router.delete("/{inventory_id}")
def delete_inventory(
    inventory_id: int,
    inventory_repo: InventoryRepository = Depends(get_inventory_repository)
):
    """Delete an inventory record"""
    inventory = inventory_repo.delete(inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    
    return {"message": "Inventory record deleted successfully"}
