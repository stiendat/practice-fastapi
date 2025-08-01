from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load biến môi trường từ file .env
load_dotenv()

# Lấy thông tin cấu hình từ biến môi trường
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = "localhost"   # vì PostgreSQL đang chạy Docker và map port ra host
DB_PORT = "5432"

# Tạo URL kết nối
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tạo engine và session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
