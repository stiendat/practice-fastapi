from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db_utils import create_database_session
from src.services.library_service import RentalService
from src.schemas.library_schemas import (
    RentalCreate, RentalResponse, RentalListResponse, ReturnBookRequest
)

router = APIRouter(prefix="/rentals", tags=["rentals"])


@router.get("/", response_model=RentalListResponse)
async def get_rentals(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    user_id: UUID = Query(None, description="Filter by user ID"),
    db: AsyncSession = Depends(create_database_session)
):
    if user_id:
        rentals = await RentalService.get_user_rentals(db, user_id)
    else:
        rentals = await RentalService.get_all_rentals(db, skip=skip, limit=limit)
    
    return RentalListResponse(rentals=rentals, total=len(rentals))


@router.get("/{rental_id}", response_model=RentalResponse)
async def get_rental(
    rental_id: UUID,
    db: AsyncSession = Depends(create_database_session)
):
    """Get rental by ID"""
    rental = await RentalService.get_rental_by_id(db, rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


@router.post("/rent", response_model=RentalResponse, status_code=201)
async def rent_book(
    rental_data: RentalCreate,
    db: AsyncSession = Depends(create_database_session)
):
    rental = await RentalService.create_rental(db, rental_data)
    if not rental:
        raise HTTPException(
            status_code=400, 
            detail="Cannot rent book. Book may not be available or user/book not found."
        )
    return rental


@router.post("/return", response_model=RentalResponse)
async def return_book(
    return_data: ReturnBookRequest,
    db: AsyncSession = Depends(create_database_session)
):
    if not return_data.rental_id and not return_data.book_id:
        raise HTTPException(
            status_code=400,
            detail="Either rental_id or book_id must be provided"
        )
    
    rental = await RentalService.return_book(db, return_data)
    if not rental:
        raise HTTPException(
            status_code=400,
            detail="Cannot return book. Rental not found or book already returned."
        )
    return rental


@router.get("/user/{user_id}", response_model=RentalListResponse)
async def get_user_rentals(
    user_id: UUID,
    active_only: bool = Query(False, description="Show only active rentals"),
    db: AsyncSession = Depends(create_database_session)
):
    rentals = await RentalService.get_user_rentals(db, user_id, active_only=active_only)
    return RentalListResponse(rentals=rentals, total=len(rentals))


@router.get("/overdue/list", response_model=RentalListResponse)
async def get_overdue_rentals(
    db: AsyncSession = Depends(create_database_session)
):
    rentals = await RentalService.get_overdue_rentals(db)
    return RentalListResponse(rentals=rentals, total=len(rentals))


@router.post("/overdue/update")
async def update_overdue_status(
    db: AsyncSession = Depends(create_database_session)
):
    count = await RentalService.update_overdue_status(db)
    return {"message": f"Updated {count} overdue rentals"}
