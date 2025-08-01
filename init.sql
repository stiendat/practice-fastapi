-- Create tables for Library Management System
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL,
    quantity INTEGER NOT NULL
);

CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_id ON books(id);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    phone VARCHAR
);

CREATE INDEX idx_users_id ON users(id);
CREATE INDEX idx_users_email ON users(email);

CREATE TABLE rentals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    book_id INTEGER NOT NULL REFERENCES books(id),
    rental_date TIMESTAMP NOT NULL DEFAULT NOW(),
    due_date TIMESTAMP NOT NULL,
    return_date TIMESTAMP,
    is_returned BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_rentals_id ON rentals(id);

-- Insert sample books data
INSERT INTO books (title, author, year, quantity) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 5),
('To Kill a Mockingbird', 'Harper Lee', 1960, 3),
('1984', 'George Orwell', 1949, 7),
('Pride and Prejudice', 'Jane Austen', 1813, 4),
('The Catcher in the Rye', 'J.D. Salinger', 1951, 2),
('Lord of the Flies', 'William Golding', 1954, 6),
('Animal Farm', 'George Orwell', 1945, 8),
('Brave New World', 'Aldous Huxley', 1932, 3),
('The Lord of the Rings', 'J.R.R. Tolkien', 1954, 2),
('Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 1997, 10);