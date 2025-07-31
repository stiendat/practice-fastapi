from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession

from src.utils.db_utils import create_database_session, db_session_context
from src.dto import borrow_dto
from src.repository.borrow_repository import borrow_repository

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/borrow/", response_model=borrow_dto.BorrowingDTO)
async def borrow_book(borrow_data: borrow_dto.BorrowingCreateDTO, db: AsyncSession = Depends(create_database_session)):
    """
    Endpoint to borrow a book.
    """
    db_session_context.set(db)
    try:
        result = await borrow_repository.create(borrow_data)
        return result
    except HTTPException as e:
        logger.error(f"Error borrowing book: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/return/", response_model=borrow_dto.BorrowingDTO)
async def return_book(borrow_id: str, db: AsyncSession = Depends(create_database_session)):
    """
    Endpoint to return a borrowed book.
    """
    db_session_context.set(db)
    try:
        result = await borrow_repository.return_book(borrow_id)
        return result
    except HTTPException as e:
        logger.error(f"Error returning book: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/borrow-all/", response_model=list[borrow_dto.BorrowingDTO])
async def get_all_borrowed_books(db: AsyncSession = Depends(create_database_session)):
    """
    Endpoint to get all borrowed books.
    """
    db_session_context.set(db)
    try:
        result = await borrow_repository.get_all()
        if not result:
            raise HTTPException(status_code=404, detail="No borrowed books found")
        return result
    except HTTPException as e:
        logger.error(f"Error fetching borrowed books: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/borrow/", response_model=borrow_dto.BorrowingDTO)
async def get_borrowed_book(borrow_id: str, db: AsyncSession = Depends(create_database_session)):
    """
    Endpoint to get a specific borrowed book by ID.
    """
    db_session_context.set(db)
    try:
        result = await borrow_repository.get_by_id(borrow_id)
        if not result:
            raise HTTPException(status_code=404, detail="Borrowed book not found")
        return result
    except HTTPException as e:
        logger.error(f"Error fetching borrowed book: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/borrow/{borrow_id}", response_model=borrow_dto.BorrowingDTO)
async def return_borrowed_book(borrow_id: str, db: AsyncSession = Depends(create_database_session)):
    """
    Endpoint to return a borrowed book.
    """
    db_session_context.set(db)
    try:
        result = await borrow_repository.return_book(borrow_id)
        if not result:
            raise HTTPException(status_code=404, detail="Borrow record not found")
        return result
    except HTTPException as e:
        logger.error(f"Error returning borrowed book: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/borrow/{borrow_id}", response_model=dict)
async def delete_borrowed_book(borrow_id: str, db: AsyncSession = Depends(create_database_session)):
    """
    Endpoint to delete a borrowed book record.
    """
    db_session_context.set(db)
    try:
        await borrow_repository.delete(borrow_id)
        return {"detail": "Borrow record deleted successfully"}
    except HTTPException as e:
        logger.error(f"Error deleting borrowed book: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/borrow/field", response_model=list[borrow_dto.BorrowingDTO])
async def get_borrowed_books_by_field(field_name: str, value: str, db: AsyncSession = Depends(create_database_session)):
    """
    Endpoint to get borrowed books by a specific field.
    """
    db_session_context.set(db)
    try:
        result = await borrow_repository.get_by_field(field_name, value)
        if not result:
            raise HTTPException(status_code=404, detail=f"No borrowed books found with {field_name} = {value}")
        return result
    except HTTPException as e:
        logger.error(f"Error fetching borrowed books by field: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/borrow/field-date", response_model=list[borrow_dto.BorrowingDTO])
async def get_borrowed_books_by_date(field_name: str, value: str, db: AsyncSession = Depends(create_database_session)):
    """
    Endpoint to get borrowed books by a specific date field.
    """
    db_session_context.set(db)
    try:
        result = await borrow_repository.get_by_field_date(field_name, value)
        if not result:
            raise HTTPException(status_code=404, detail=f"No borrowed books found with {field_name} = {value}")
        return result
    except HTTPException as e:
        logger.error(f"Error fetching borrowed books by date: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")