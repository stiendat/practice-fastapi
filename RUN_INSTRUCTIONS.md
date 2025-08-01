# Library Management System - Setup Instructions

## Prerequisites
- Python 3.8+
- Docker and Docker Compose
- PostgreSQL (via Docker)

## Setup Steps

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start PostgreSQL Database:**
   ```bash
   docker-compose up -d
   ```

3. **Initialize Database Tables:**
   ```bash
   python cli.py init_database
   ```

4. **Import Initial Data:**
   ```bash
   python cli.py import_data
   ```

5. **Start the FastAPI Server:**
   ```bash
   uvicorn main:app --reload
   ```

## CLI Commands

### PostgreSQL Commands (Production)
- `python cli.py init_database` - Create PostgreSQL database tables
- `python cli.py import_data` - Import books from CSV to PostgreSQL
- `python cli.py run_test` - Run all tests

### SQLite Commands (Development/Testing)  
- `python cli.py init_sqlite` - Create SQLite database tables
- `python cli.py import_sqlite` - Import books from CSV to SQLite

## Quick Start (SQLite)

For quick testing without PostgreSQL:

1. **Initialize SQLite Database:**
   ```bash
   python cli.py init_sqlite
   ```

2. **Import Sample Data:**
   ```bash
   python cli.py import_sqlite
   ```

3. **Start Server with SQLite:**
   ```bash
   USE_SQLITE=true uvicorn main:app --reload
   ```

## API Endpoints

### Books Management
- `GET /books` - Get all books
- `GET /books/{book_id}` - Get book by ID
- `POST /books` - Create new book

### Users Management  
- `GET /users` - Get all users
- `POST /users` - Create new user

### Rentals Management
- `POST /rentals/rent` - Rent a book
- `POST /rentals/return` - Return a book

## API Documentation
Once the server is running, visit:
- Interactive API docs: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## Data Models

### Book
- id: Integer (Primary Key)
- title: String
- author: String  
- year: Integer
- quantity: Integer

### User
- id: Integer (Primary Key)
- full_name: String
- email: String (Unique)
- phone: String (Optional)

### Rental
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key)
- book_id: Integer (Foreign Key)
- rental_date: DateTime
- due_date: DateTime
- return_date: DateTime (Optional)
- is_returned: Boolean