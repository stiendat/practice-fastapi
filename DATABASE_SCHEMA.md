## Models Overview

### 1. User Model
```python
class User(Base):
    __tablename__ = "users"
    
    # Primary Key
    id = UUID (Primary Key, Default: uuid4)
    
    # User Information
    name = String(255), Not Null
    email = String(255), Unique, Not Null
    phone = String(20), Nullable
    address = Text, Nullable
    
    # Timestamps
    created_at = DateTime, Default: utcnow
    updated_at = DateTime, Default: utcnow, onupdate
```

### 2. Book Model
```python
class Book(Base):
    __tablename__ = "books"
    
    # Primary Key
    id = UUID (Primary Key, Default: uuid4)
    
    # Book Information
    title = String(500), Not Null
    author = String(255), Not Null
    isbn = String(20), Unique, Not Null
    publication_year = Integer, Nullable
    publisher = String(255), Nullable
    
    # Image URLs
    image_url_s = String(500), Nullable  # Small
    image_url_m = String(500), Nullable  # Medium
    image_url_l = String(500), Nullable  # Large
    
    # Availability
    is_available = Boolean, Default: True
    
    # Timestamps
    created_at = DateTime, Default: utcnow
    updated_at = DateTime, Default: utcnow, onupdate
```

### 3. Rental Model
```python
class Rental(Base):
    __tablename__ = "rentals"
    
    # Primary Key
    id = UUID (Primary Key, Default: uuid4)
    
    # Foreign Keys
    user_id = UUID, ForeignKey("users.id"), Not Null
    book_id = UUID, ForeignKey("books.id"), Not Null
    
    # Rental Information
    rent_date = DateTime, Default: utcnow
    return_date = DateTime, Nullable
    due_date = DateTime, Not Null
    status = ENUM(RentalStatus), Default: RENTED
    
    # Timestamps
    created_at = DateTime, Default: utcnow
    updated_at = DateTime, Default: utcnow, onupdate
```

## Enum Types

### RentalStatus
```python
class RentalStatus(str, Enum):
    RENTED = "RENTED"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"
```

## Relationships

### User - Rental (One-to-Many)
- Một User có thể có nhiều Rentals
- `User.rentals` -> List[Rental]
- `Rental.user` -> User

### Book - Rental (One-to-Many)
- Một Book có thể có nhiều Rentals (lịch sử mượn)
- `Book.rentals` -> List[Rental]
- `Rental.book` -> Book

### User - Book (Many-to-Many through Rental)
- User và Book liên kết qua bảng Rental
- Tracking: rent_date, return_date, status

## Database Constraints

### Primary Keys
- Tất cả tables dùng UUID primary key
- Auto-generated với uuid4()

### Unique Constraints
- `users.email` - Email duy nhất
- `books.isbn` - ISBN duy nhất

### Foreign Keys
- `rentals.user_id` -> `users.id`
- `rentals.book_id` -> `books.id`

### Default Values
- Timestamps: `datetime.utcnow`
- `book.is_available`: `True`
- `rental.status`: `RENTED`

