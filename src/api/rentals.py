from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from src.schemas.rental import RentalCreate, RentalResponse, ReturnRequest
from src.repositories.rental_repository import RentalRepository
from src.dependencies import get_rental_repository

router = APIRouter(prefix="/rentals", tags=["rentals"])

@router.post("/rent", response_model=RentalResponse)
def rent_books(
    rental_request: RentalCreate, 
    rental_repo: RentalRepository = Depends(get_rental_repository)
):
    """Create a new rental (borrow books)"""
    try:
        rental = rental_repo.create_rental(
            user_id=rental_request.user_id,
            book_ids=rental_request.book_ids,
            due_date=rental_request.due_date
        )
        return rental
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create rental: {str(e)}")

@router.post("/return")
def return_books(
    return_request: ReturnRequest, 
    rental_repo: RentalRepository = Depends(get_rental_repository)
):
    """Return books - either entire rental or specific book copies"""
    try:
        if return_request.rental_id:
            # Return entire rental
            result = rental_repo.return_rental(return_request.rental_id)
            return result
        
        elif return_request.book_copy_ids:
            # Return specific book copies
            result = rental_repo.return_book_copies(return_request.book_copy_ids)
            return result
        
        else:
            raise HTTPException(
                status_code=400, 
                detail="Must provide either rental_id or book_copy_ids"
            )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to return books: {str(e)}")

@router.get("/", response_model=List[RentalResponse])
def get_rentals(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    include_returned: bool = Query(False, description="Include already returned rentals"),
    rental_repo: RentalRepository = Depends(get_rental_repository)
):
    """Get all rentals with pagination"""
    if include_returned:
        rentals = rental_repo.get_all(skip=skip, limit=limit)
    else:
        # Get only active (non-returned) rentals
        rentals = rental_repo.get_all(skip=skip, limit=limit)
        rentals = [r for r in rentals if not r.return_date]
    
    return rentals

@router.get("/overdue", response_model=List[RentalResponse])
def get_overdue_rentals(rental_repo: RentalRepository = Depends(get_rental_repository)):
    """Get all overdue rentals"""
    rentals = rental_repo.get_overdue_rentals()
    return rentals

@router.get("/user/{user_id}", response_model=List[RentalResponse])
def get_user_rentals(
    user_id: int,
    include_returned: bool = Query(False, description="Include already returned rentals"),
    rental_repo: RentalRepository = Depends(get_rental_repository)
):
    """Get all rentals for a specific user"""
    rentals = rental_repo.get_user_rentals(user_id, include_returned=include_returned)
    return rentals

@router.get("/{rental_id}", response_model=RentalResponse)
def get_rental(
    rental_id: int, 
    rental_repo: RentalRepository = Depends(get_rental_repository)
):
    """Get a specific rental with all its details"""
    rental = rental_repo.get_rental_with_items(rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental
