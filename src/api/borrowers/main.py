from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from src.models import Borrower
from src.utils.db_utils import create_database_session
from src.api.borrowers.schemas import BorrowerCreate, BorrowerResponse

router = APIRouter(prefix="/users", tags=["borrowers"])


@router.get("/", response_model=List[BorrowerResponse])
async def get_borrowers(session: AsyncSession = Depends(create_database_session)):
    result = await session.execute(select(Borrower))
    borrowers = result.scalars().all()
    return borrowers


@router.post("/", response_model=BorrowerResponse, status_code=status.HTTP_201_CREATED)
async def create_borrower(borrower_data: BorrowerCreate, session: AsyncSession = Depends(create_database_session)):
    # Check if a borrower with the same email already exists
    result = await session.execute(select(Borrower).where(Borrower.email == borrower_data.email))
    existing_borrower = result.scalar_one_or_none()

    if existing_borrower:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Borrower with email {borrower_data.email} already exists"
        )

    # Create new borrower
    new_borrower = Borrower(**borrower_data.dict())
    session.add(new_borrower)
    await session.commit()
    await session.refresh(new_borrower)

    return new_borrower
