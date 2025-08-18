# Library Management System - FastAPI Backend

Repo này sử dụng để lưu trữ bài tập cho phần Lập trình Backend sử dụng FastAPI.

## Nội dung bài tập

Nội dung bài tập được ghi trong file `Practice.md` trong thư mục gốc của repo này.

## Cách làm bài

1. Fork repo này về tài khoản của bạn.
2. Thực hiện chỉnh sửa project theo yêu cầu trong file `Practice.md`.
3. Commit và push code lên repo của bạn.
4. Tạo Pull Request tới repo này, trỏ tới nhánh bài tập tương ứng.
5. Copy link PR và gửi trong form bài tập.

## Thiết lập môi trường

### 1. Tạo file .env
Tạo file `.env` trong thư mục gốc với nội dung:
```
POSTGRES_PASSWORD=password
POSTGRES_USER=user
POSTGRES_DB=library_db
```

### 2. Khởi động PostgreSQL
```bash
docker-compose up -d
```

### 3. Khởi tạo database
```bash
python cli.py init_database
```

### 4. Test database
```bash
python cli.py test_database
```

## Cấu trúc dự án

```
library-fastapi-week3/
├── src/
│   ├── models/          # SQLAlchemy models
│   │   ├── book.py      # Book model
│   │   ├── user.py      # User model
│   │   └── rental.py    # Rental model
│   ├── utils/           # Utility functions
│   │   ├── db_utils.py  # Database utilities
│   │   └── helpers.py   # Helper functions
│   └── api/             # FastAPI routes (TODO)
├── commands/            # CLI commands
├── test_data/           # Sample data
├── docker-compose.yaml  # Docker configuration
├── cli.py              # CLI interface
└── test_database.py    # Database tests
```

## Data Model

### ERD (Entity Relationship Diagram)
```
Users (1) -------- (N) Rentals (N) -------- (1) Books
```

### Các bảng:
- **Books**: Lưu thông tin sách (ISBN, title, author, quantity, etc.)
- **Users**: Lưu thông tin người mượn (name, email, phone)
- **Rentals**: Lưu thông tin mượn/trả sách (user_id, book_id, dates, status)

Chi tiết thiết kế xem trong file `DATABASE_SETUP.md`.

## Các lệnh CLI

- `python cli.py init_database`: Khởi tạo database và import dữ liệu
- `python cli.py test_database`: Test kết nối database và models
- `python cli.py run_test`: Chạy tests (TODO)

## Tiếp theo

- [ ] Xây dựng FastAPI endpoints
- [ ] Tạo Pydantic schemas
- [ ] Implement business logic
- [ ] Viết tests
- [ ] Tạo documentation