"""
Rental management API endpoints
"""

from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.library_models import get_async_session
from src.schemas.library_schemas import (
    RentalResponse, RentalCreate, RentalReturn, RentalsListResponse,
    APIResponse
)
from src.services.library_service import RentalService

router = APIRouter(prefix="/rentals", tags=["Rentals"])


async def get_db():
    """Dependency to get async database session"""
    async with get_async_session() as db:
        yield db


@router.get("/", response_model=RentalsListResponse)
async def get_rentals(
    skip: int = Query(0, ge=0, description="Number of rentals to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of rentals to return"),
    active_only: bool = Query(False, description="Show only active rentals"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of rentals with pagination
    """
    try:
        if active_only:
            rentals = await RentalService.get_active_rentals(db, skip, limit)
        else:
            rentals = await RentalService.get_rentals(db, skip, limit)
        
        return RentalsListResponse(
            total=len(rentals),
            rentals=[RentalResponse.model_validate(rental) for rental in rentals]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{rental_id}", response_model=RentalResponse)
async def get_rental(rental_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific rental by ID
    """
    rental = await RentalService.get_rental_by_id(db, rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    
    return RentalResponse.model_validate(rental)


@router.post("/rent", response_model=RentalResponse, status_code=201)
async def create_rental(rental: RentalCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new rental (rent a book)
    """
    try:
        db_rental = await RentalService.create_rental(db, rental)
        if not db_rental:
            raise HTTPException(
                status_code=400,
                detail="Cannot create rental. Book may not be available or user may not exist."
            )
        
        return RentalResponse.model_validate(db_rental)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create rental: {str(e)}")


@router.post("/rent-simple", response_model=RentalResponse, status_code=201)
async def create_simple_rental(
    user_id: int,
    book_id: int,
    days: int = Query(14, ge=1, le=90, description="Number of days to rent"),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a rental with automatic return date calculation
    """
    try:
        rental_data = RentalCreate(
            user_id=user_id,
            book_id=book_id,
            expected_return_date=date.today() + timedelta(days=days)
        )
        
        db_rental = await RentalService.create_rental(db, rental_data)
        if not db_rental:
            raise HTTPException(
                status_code=400,
                detail="Cannot create rental. Book may not be available or user may not exist."
            )
        
        return RentalResponse.model_validate(db_rental)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create rental: {str(e)}")


@router.post("/{rental_id}/return", response_model=RentalResponse)
async def return_book(
    rental_id: int,
    return_data: RentalReturn = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Return a book
    """
    try:
        if return_data is None:
            return_data = RentalReturn()
        
        returned_rental = RentalService.return_book(db, rental_id, return_data)
        if not returned_rental:
            raise HTTPException(
                status_code=400,
                detail="Cannot return book. Rental may not exist or book may already be returned."
            )
        
        return RentalResponse.model_validate(returned_rental)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to return book: {str(e)}")


@router.get("/overdue/list", response_model=RentalsListResponse)
async def get_overdue_rentals(db: AsyncSession = Depends(get_db)):
    """
    Get all overdue rentals
    """
    try:
        overdue_rentals = await RentalService.get_overdue_rentals(db)
        return RentalsListResponse(
            total=len(overdue_rentals),
            rentals=[RentalResponse.model_validate(rental) for rental in overdue_rentals]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get overdue rentals: {str(e)}")


@router.post("/overdue/update-status", response_model=APIResponse)
async def update_overdue_status(db: AsyncSession = Depends(get_db)):
    """
    Update status of overdue rentals
    """
    try:
        updated_count = await RentalService.update_overdue_status(db)
        return APIResponse(
            success=True,
            message=f"Updated {updated_count} overdue rentals",
            data={"updated_count": updated_count}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update overdue status: {str(e)}")


# Convenience endpoints
@router.post("/quick-rent")
async def quick_rent(
    user_email: str,
    book_isbn: str,
    days: int = Query(14, ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    """
    Quick rent using email and ISBN
    """
    try:
        from src.services.library_service import UserService, BookService
        
        # Find user by email
        user = await UserService.get_user_by_email(db, user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Find book by ISBN
        book = await BookService.get_book_by_isbn(db, book_isbn)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Create rental
        rental_data = RentalCreate(
            user_id=user.id,
            book_id=book.id,
            expected_return_date=date.today() + timedelta(days=days)
        )
        
        db_rental = await RentalService.create_rental(db, rental_data)
        if not db_rental:
            raise HTTPException(
                status_code=400,
                detail="Cannot create rental. Book may not be available."
            )
        
        return RentalResponse.model_validate(db_rental)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create quick rental: {str(e)}")
