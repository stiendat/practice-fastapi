from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import books_router, users_router, rentals_router

app = FastAPI(
    title="Library Management System API",
    description="API quản lý thư viện với các chức năng mượn/trả sách",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router)
app.include_router(users_router)
app.include_router(rentals_router)


@app.get("/")
async def root():
    return {
        "message": "Library Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
