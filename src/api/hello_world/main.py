from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.utils.db_utils import create_database_session

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World", "status": "API is working!"}
