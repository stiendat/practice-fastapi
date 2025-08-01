from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class InventoryBase(BaseModel):
    book_id: int
    total_copies: int = Field(ge=0, description="Total number of copies")
    available_copies: int = Field(ge=0, description="Number of available copies")
    borrowed_copies: int = Field(ge=0, description="Number of borrowed copies")
    lost_copies: int = Field(ge=0, description="Number of lost copies")
    damaged_copies: int = Field(ge=0, description="Number of damaged copies")

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    """Schema for updating inventory - all fields optional"""
    total_copies: Optional[int] = Field(None, ge=0)
    available_copies: Optional[int] = Field(None, ge=0)
    borrowed_copies: Optional[int] = Field(None, ge=0)
    lost_copies: Optional[int] = Field(None, ge=0)
    damaged_copies: Optional[int] = Field(None, ge=0)

class InventoryResponse(InventoryBase):
    id: int
    created_at: datetime
    modified_at: datetime
    
    class Config:
        from_attributes = True

class InventoryWithBookResponse(BaseModel):
    """Response model for inventory with book information"""
    # Inventory information
    id: int
    book_id: int
    total_copies: int
    available_copies: int
    borrowed_copies: int
    lost_copies: int
    damaged_copies: int
    created_at: datetime
    modified_at: datetime
    
    # Book information
    book_title: str
    book_author: str
    book_isbn: str
    book_publisher: Optional[str] = None
    
    class Config:
        from_attributes = True

class InventoryAdjustment(BaseModel):
    """Schema for adjusting inventory counts"""
    adjustment_type: str = Field(..., pattern="^(add|remove|set)$", description="Type of adjustment: add, remove, or set")
    copy_type: str = Field(..., pattern="^(total_copies|available_copies|borrowed_copies|lost_copies|damaged_copies)$", description="Which copy type to adjust")
    amount: int = Field(..., ge=0, description="Amount to adjust")
    reason: Optional[str] = Field(None, description="Reason for adjustment")

class InventoryStats(BaseModel):
    """Overall inventory statistics"""
    total_books: int
    total_copies_all_books: int
    total_available_all_books: int
    total_borrowed_all_books: int
    total_lost_all_books: int
    total_damaged_all_books: int
    books_with_no_copies: int
    books_out_of_stock: int
    utilization_rate: float = Field(..., description="Percentage of copies currently borrowed")

class LowStockAlert(BaseModel):
    """Alert for books with low stock"""
    book_id: int
    book_title: str
    book_author: str
    available_copies: int
    total_copies: int
    threshold_violated: int
