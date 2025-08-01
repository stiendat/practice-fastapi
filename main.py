from fastapi import FastAPI
from src.api.main_router import api_router
from src.utils.db_utils import Base, async_engine

app = FastAPI(
    title="Library Management System",
    description="A comprehensive library management system built with FastAPI",
    version="1.0.0"
)

# Include API routes
app.include_router(api_router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Library Management System API", 
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Create tables on startup
@app.on_event("startup")
async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

