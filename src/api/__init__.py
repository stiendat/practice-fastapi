from .books import router as books_router
from .users import router as users_router
from .rentals import router as rentals_router

__all__ = ["books_router", "users_router", "rentals_router"]
