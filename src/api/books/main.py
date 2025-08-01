from typing import List
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from models.schemas import *

from src.utils.db_utils import create_database_session

router = APIRouter()

@router.get("/", response_model=List[BookRead])
async def get_books(
    
):
    return {"message": "Hello World"}
