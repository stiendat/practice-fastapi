from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db_utils import create_database_session
from src.services.rental_service import RentalService
from src.schemas import RentalCreate, RentalReturn, RentalResponse, RentalListResponse

router = APIRouter(prefix="/rentals", tags=["rentals"])


async def get_rental_service(session: AsyncSession = Depends(create_database_session)) -> RentalService:
    return RentalService(session)


@router.get("/", response_model=RentalListResponse)
async def get_rentals(
    page: int = Query(1, ge=1, description="Số trang"),
    size: int = Query(10, ge=1, le=100, description="Số lượng item mỗi trang"),
    rental_service: RentalService = Depends(get_rental_service)
):
    """Lấy danh sách tất cả lần mượn"""
    skip = (page - 1) * size
    rentals, total = await rental_service.get_all_rentals(skip=skip, limit=size)
    
    return RentalListResponse(
        rentals=[RentalResponse.model_validate(rental) for rental in rentals],
        total=total,
        page=page,
        size=size
    )


@router.get("/{rental_id}", response_model=RentalResponse)
async def get_rental(
    rental_id: str,
    rental_service: RentalService = Depends(get_rental_service)
):
    """Lấy thông tin chi tiết một lần mượn"""
    rental = await rental_service.get_rental_by_id(rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail=f"Lần mượn với ID {rental_id} không tồn tại")
    
    return RentalResponse.model_validate(rental)


@router.post("/rent", response_model=RentalResponse, status_code=201)
async def create_rental(
    rental_data: RentalCreate,
    rental_service: RentalService = Depends(get_rental_service)
):
    """Tạo lần mượn sách mới"""
    try:
        rental = await rental_service.create_rental(rental_data)
        return RentalResponse.model_validate(rental)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")


@router.post("/return", response_model=RentalResponse)
async def return_book(
    return_data: RentalReturn,
    rental_service: RentalService = Depends(get_rental_service)
):
    """Ghi nhận trả sách"""
    try:
        rental = await rental_service.return_book(return_data)
        return RentalResponse.model_validate(rental)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")


@router.get("/user/{user_id}", response_model=List[RentalResponse])
async def get_user_rentals(
    user_id: str,
    rental_service: RentalService = Depends(get_rental_service)
):
    """Lấy danh sách lần mượn của một người dùng"""
    rentals = await rental_service.get_user_rentals(user_id)
    return [RentalResponse.model_validate(rental) for rental in rentals]


@router.get("/overdue/list", response_model=List[RentalResponse])
async def get_overdue_rentals(
    rental_service: RentalService = Depends(get_rental_service)
):
    """Lấy danh sách sách quá hạn"""
    rentals = await rental_service.get_overdue_rentals()
    return [RentalResponse.model_validate(rental) for rental in rentals] 