from typing import Any

from src.models.book_models import BookModel
from src.dto.book_dto import BookUpdateDTO, BookCreateDTO
from src.repository.base_repository import BaseRepository, ModelType

import logging

logger = logging.getLogger(__name__)

class BookRepository(BaseRepository[BookModel, BookCreateDTO, BookUpdateDTO]):
    def __init__(self):
        super().__init__(BookModel)
        logger.debug("BookRepository initialized")


book_repository = BookRepository()