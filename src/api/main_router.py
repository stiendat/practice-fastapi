from fastapi import FastAPI
from model.database import Base, engine
from api.route import books
# Tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include router
app.include_router(books.router)
