# Library Management System - FastAPI Practice

Repo này sử dụng để lưu trữ bài tập cho phần Lập trình Backend sử dụng FastAPI.

## 📋 Mô tả dự án

Hệ thống backend quản lý thư viện được xây dựng với FastAPI, hỗ trợ các chức năng:

- **Quản lý Sách**: CRUD operations cho sách, tìm kiếm, kiểm tra tồn kho
- **Quản lý Người dùng**: CRUD operations cho người mượn sách
- **Quản lý Mượn/Trả**: Xử lý quy trình mượn và trả sách, theo dõi quá hạn

## 🏗️ Kiến trúc hệ thống

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FastAPI   │    │ SQLAlchemy  │    │ PostgreSQL  │
│   (API)     │◄──►│  (ORM)      │◄──►│ (Database)  │
└─────────────┘    └─────────────┘    └─────────────┘
       ▲
       │
   ┌─────────────┐
   │  Pydantic   │
   │ (Validation)│
   └─────────────┘
```

## 🚀 Cách chạy dự án

### 1. Chuẩn bị
```bash
git clone <repository-url>
cd practice-fastapi
```

### 2. Khởi động Database
```bash
docker-compose up -d
```

### 3. Cài đặt dependencies
```bash
uv sync
# hoặc
pip install -r requirements.txt
```

### 4. Thiết lập Database
```bash
python cli.py create_tables
python cli.py import_books
```

### 5. Chạy ứng dụng
```bash
uvicorn main:app --reload
```

Truy cập:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📊 Data Model (ERD)

```
Books (1) ────── (N) Rentals (N) ────── (1) Users
  │                     │                    │
  ├─ id (PK)           ├─ id (PK)           ├─ id (PK)
  ├─ title             ├─ book_id (FK)      ├─ full_name
  ├─ author            ├─ user_id (FK)      ├─ email
  ├─ publication_year  ├─ rent_date         ├─ phone_number
  ├─ isbn              ├─ expected_return   ├─ address
  ├─ quantity          ├─ actual_return     ├─ is_active
  ├─ available_qty     ├─ status           └─ timestamps
  └─ timestamps        └─ notes
```

## 🔗 API Endpoints

### Books
- `GET /api/v1/books/` - Danh sách sách (có pagination, search)
- `POST /api/v1/books/` - Thêm sách mới
- `GET /api/v1/books/{id}` - Chi tiết sách
- `PUT /api/v1/books/{id}` - Cập nhật sách
- `DELETE /api/v1/books/{id}` - Xóa sách

### Users  
- `GET /api/v1/users/` - Danh sách người dùng
- `POST /api/v1/users/` - Thêm người dùng
- `GET /api/v1/users/{id}` - Chi tiết người dùng
- `PUT /api/v1/users/{id}` - Cập nhật người dùng
- `DELETE /api/v1/users/{id}` - Vô hiệu hóa người dùng

### Rentals
- `POST /api/v1/rentals/rent` - Mượn sách
- `POST /api/v1/rentals/{id}/return` - Trả sách
- `GET /api/v1/rentals/overdue/list` - Sách quá hạn
- `POST /api/v1/rentals/quick-rent` - Mượn nhanh bằng email/ISBN

## 📁 Cấu trúc Project

```
practice-fastapi/
├── src/
│   ├── api/           # API endpoints
│   ├── models/        # SQLAlchemy models  
│   ├── schemas/       # Pydantic schemas
│   └── services/      # Business logic
├── scripts/           # Utility scripts
├── test_data/         # Sample data
├── main.py           # FastAPI app
├── cli.py            # CLI commands
└── docker-compose.yaml
```

## 📖 Tài liệu chi tiết

- [Setup Guide](SETUP_GUIDE.md) - Hướng dẫn chi tiết cài đặt và sử dụng
- [Practice.md](Practice.md) - Đề bài và yêu cầu

## 🎯 Cách nộp bài

1. Fork repo này về tài khoản của bạn
2. Thực hiện chỉnh sửa project theo yêu cầu
3. Commit và push code lên repo của bạn
4. Tạo Pull Request tới repo này
5. Copy link PR và gửi trong form bài tập