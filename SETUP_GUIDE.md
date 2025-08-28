# Library Management System - Setup Guide

## Tổng quan

Hệ thống quản lý thư viện được xây dựng bằng FastAPI với các chức năng chính:
- Quản lý sách (Books)
- Quản lý người dùng (Users) 
- Quản lý mượn/trả sách (Rentals)

## Cấu trúc dự án

```
practice-fastapi/
├── src/
│   ├── api/                    # API endpoints
│   │   ├── books.py           # Book management APIs
│   │   ├── users.py           # User management APIs
│   │   └── rentals.py         # Rental management APIs
│   ├── models/                 # Database models
│   │   └── library_models.py  # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   │   └── library_schemas.py # Request/Response schemas
│   ├── services/               # Business logic
│   │   └── library_service.py # Service layer
│   └── utils/                  # Utilities
│       └── db_utils.py        # Database connection
├── commands/                   # CLI commands and scripts
│   └── init_database/         # Database initialization
│       ├── main.py           # Main init script
│       └── init.py           # CSV import script
├── test_data/                  # Test data
│   └── books.csv              # Sample books data
├── .env                       # Environment variables
├── docker-compose.yaml        # Docker configuration
├── main.py                    # FastAPI application
├── cli.py                     # CLI commands
├── settings.py                # Configuration settings
├── init_db.py                 # Simple database init
└── requirements.txt           # Python dependencies
```

## ERD (Entity Relationship Diagram)

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    Books    │       │   Rentals   │       │    Users    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │◄──────┤ book_id (FK)│       │ id (PK)     │
│ title       │       │ user_id (FK)├──────►│ full_name   │
│ author      │       │ rent_date   │       │ email       │
│ isbn        │       │ expected_   │       │ phone_number│
│ pub_year    │       │ return_date │       │ address     │
│ publisher   │       │ actual_     │       │ is_active   │
│ category    │       │ return_date │       │ created_at  │
│ total_copies│       │ status      │       │ updated_at  │
│ available_  │       │ notes       │       └─────────────┘
│ copies      │       │ created_at  │
│ image_urls  │       │ updated_at  │
│ description │       └─────────────┘
│ created_at  │
│ updated_at  │
└─────────────┘
```

## Cài đặt và Chạy

### 1. Chuẩn bị môi trường

```bash
# Clone repository
git clone <repo-url>
cd practice-fastapi

# Kiểm tra file .env (đã có sẵn):
# POSTGRES_PASSWORD=password
# POSTGRES_USER=postgres
# POSTGRES_DB=postgres
```

### 2. Khởi động PostgreSQL bằng Docker

```bash
# Khởi động database
docker-compose up -d

# Kiểm tra container đang chạy
docker-compose ps

# PostgreSQL sẽ chạy trên port 5431 (mapped từ 5432)
```

### 3. Cài đặt dependencies

```bash
# Cài đặt Python packages
pip install -r requirements.txt

# Dependencies chính:
# - fastapi
# - uvicorn
# - sqlalchemy
# - psycopg2-binary
# - pydantic[email]
# - python-dotenv
```

### 4. Tạo database tables

```bash
# Sử dụng CLI command
python cli.py init_database

# Hoặc sử dụng advanced init với CSV import
python commands/init_database/init.py
```

### 5. Import dữ liệu mẫu (tùy chọn)

```bash
# Import books từ CSV (nếu có file test_data/books.csv)
python commands/init_database/init.py

# Hoặc sử dụng CLI
python cli.py import_books
```

### 6. Chạy ứng dụng

```bash
# Chạy development server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Ứng dụng sẽ chạy tại:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

## Cấu hình Database

### Connection Settings (settings.py)
```python
POSTGRES_PASSWORD = "password"     # từ .env
POSTGRES_USER = "postgres"         # từ .env
POSTGRES_DB = "postgres"           # từ .env
POSTGRES_HOST = "localhost"        # default
POSTGRES_PORT = "5431"             # mapped port
```

### Database URL
- **Synchronous**: `postgresql://postgres:password@localhost:5431/postgres`
- **Connection port**: `5431` (Docker maps 5432→5431)

## API Endpoints

### Books Management
- `GET /api/v1/books/` - Lấy danh sách sách (có pagination và search)
- `GET /api/v1/books/{book_id}` - Lấy thông tin chi tiết sách
- `POST /api/v1/books/` - Thêm sách mới
- `PUT /api/v1/books/{book_id}` - Cập nhật thông tin sách
- `DELETE /api/v1/books/{book_id}` - Xóa sách
- `GET /api/v1/books/{book_id}/availability` - Kiểm tra tình trạng sách

### Users Management
- `GET /api/v1/users/` - Lấy danh sách người dùng
- `GET /api/v1/users/{user_id}` - Lấy thông tin chi tiết người dùng
- `POST /api/v1/users/` - Thêm người dùng mới
- `PUT /api/v1/users/{user_id}` - Cập nhật thông tin người dùng
- `DELETE /api/v1/users/{user_id}` - Vô hiệu hóa người dùng
- `GET /api/v1/users/{user_id}/rentals` - Lấy lịch sử mượn sách của người dùng

### Rentals Management
- `GET /api/v1/rentals/` - Lấy danh sách mượn sách
- `GET /api/v1/rentals/{rental_id}` - Lấy thông tin chi tiết một lần mượn
- `POST /api/v1/rentals/rent` - Tạo phiếu mượn sách mới
- `POST /api/v1/rentals/rent-simple` - Mượn sách với ngày trả tự động
- `POST /api/v1/rentals/{rental_id}/return` - Trả sách
- `GET /api/v1/rentals/overdue/list` - Lấy danh sách sách quá hạn
- `POST /api/v1/rentals/overdue/update-status` - Cập nhật trạng thái quá hạn
- `POST /api/v1/rentals/quick-rent` - Mượn sách nhanh bằng email và ISBN

## CLI Commands

```bash
# Khởi tạo database với sample data
python cli.py init_database

# Import books từ CSV
python cli.py import_books

# Tạo tables
python cli.py create_tables

# Test API endpoints
python cli.py run_test
```

## Ví dụ sử dụng API

### 1. Thêm người dùng mới

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Nguyễn Văn A",
    "email": "nguyenvana@example.com",
    "phone_number": "0123456789",
    "address": "123 Đường ABC, Quận 1, TP.HCM"
  }'
```

### 2. Thêm sách mới

```bash
curl -X POST "http://localhost:8000/api/v1/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Lập trình Python",
    "author": "Nguyễn Văn B",
    "isbn": "9781234567890",
    "publication_year": 2023,
    "publisher": "NXB Công nghệ",
    "category": "Programming",
    "total_copies": 3,
    "description": "Sách hướng dẫn lập trình Python cơ bản"
  }'
```

### 3. Mượn sách đơn giản

```bash
curl -X POST "http://localhost:8000/api/v1/rentals/rent-simple?user_id=1&book_id=1&days=14"
```

### 4. Trả sách

```bash
curl -X POST "http://localhost:8000/api/v1/rentals/1/return" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Sách được trả trong tình trạng tốt"
  }'
```

### 5. Tìm kiếm sách

```bash
curl "http://localhost:8000/api/v1/books/?search=python&limit=5&category=Programming"
```

## Database Schema

### Books Table
```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    publication_year INTEGER,
    publisher VARCHAR(255),
    category VARCHAR(100) DEFAULT 'General',
    total_copies INTEGER NOT NULL DEFAULT 1,
    available_copies INTEGER NOT NULL DEFAULT 1,
    image_url_s VARCHAR(500),
    image_url_m VARCHAR(500),
    image_url_l VARCHAR(500),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Rentals Table
```sql
CREATE TABLE rentals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    book_id INTEGER REFERENCES books(id),
    rent_date DATE DEFAULT CURRENT_DATE,
    expected_return_date DATE NOT NULL,
    actual_return_date DATE,
    status VARCHAR(20) DEFAULT 'rented',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Testing

### Automated Testing
```bash
# Test tất cả API endpoints
python cli.py run_test
```

### Manual Testing
1. **Swagger UI**: http://localhost:8000/docs
2. **ReDoc**: http://localhost:8000/redoc
3. **Postman**: Import từ http://localhost:8000/openapi.json

## Troubleshooting

### Database Connection Issues
```bash
# Kiểm tra PostgreSQL container
docker-compose logs db

# Restart PostgreSQL
docker-compose restart db

# Kiểm tra port
netstat -an | grep 5431
```

### Import Errors
```bash
# Đảm bảo PYTHONPATH đúng
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Hoặc chạy từ thư mục root
cd /path/to/practice-fastapi
python -m uvicorn main:app --reload
```

## Project Architecture

### Synchronous Design
- **Database**: PostgreSQL với psycopg2-binary
- **ORM**: SQLAlchemy (synchronous)
- **API**: FastAPI với sync endpoints
- **Session Management**: Standard SQLAlchemy sessions

### Key Files
- `main.py`: FastAPI application entry point
- `settings.py`: Configuration management
- `src/utils/db_utils.py`: Database connection utilities
- `src/models/library_models.py`: SQLAlchemy models
- `src/schemas/library_schemas.py`: Pydantic schemas
- `src/services/library_service.py`: Business logic layer

## Deployment Notes

### Environment Variables
```bash
# Production .env
POSTGRES_PASSWORD=secure_password_here
POSTGRES_USER=library_user
POSTGRES_DB=library_production
POSTGRES_HOST=production-db-host
POSTGRES_PORT=5432
```

### Docker Production
```bash
# Build production image
docker build -t library-api .

# Run with production settings
docker run -d -p 8000:8000 --env-file .env library-api
```
