from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import books, users, rentals

app = FastAPI(
    title="Library Management System",
    description="A comprehensive API for managing library books, users, and rentals",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(books.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(rentals.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Library Management System API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}