import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"


def test_book_api():
    print("Testing Book API...")

    # Test creating a new book
    book_data = {
        "isbn": "1234567890",
        "title": "Test Book",
        "author": "Test Author",
        "year_of_publication": 2023,
        "publisher": "Test Publisher",
        "img_url_s": "http://example.com/small.jpg",
        "img_url_m": "http://example.com/medium.jpg",
        "img_url_l": "http://example.com/large.jpg",
        "total_quantity": 5,
        "available_quantity": 5
    }

    response = requests.post(f"{BASE_URL}/books/", json=book_data)
    print(f"Create book response: {response.status_code}")
    if response.status_code == 201:
        book = response.json()
        book_id = book["id"]
        print(f"Created book with ID: {book_id}")

        # Test getting the book
        response = requests.get(f"{BASE_URL}/books/{book_id}")
        print(f"Get book response: {response.status_code}")
        if response.status_code == 200:
            print("Book retrieved successfully")

        # Test getting all books
        response = requests.get(f"{BASE_URL}/books/")
        print(f"Get all books response: {response.status_code}")
        if response.status_code == 200:
            books = response.json()
            print(f"Retrieved {len(books)} books")

    print("")


def test_borrower_api():
    print("Testing Borrower API...")

    # Test creating a new borrower
    borrower_data = {
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "phone_number": "+1234567890"
    }

    response = requests.post(f"{BASE_URL}/users/", json=borrower_data)
    print(f"Create borrower response: {response.status_code}")
    if response.status_code == 201:
        borrower = response.json()
        borrower_id = borrower["id"]
        print(f"Created borrower with ID: {borrower_id}")

        # Test getting all borrowers
        response = requests.get(f"{BASE_URL}/users/")
        print(f"Get all borrowers response: {response.status_code}")
        if response.status_code == 200:
            borrowers = response.json()
            print(f"Retrieved {len(borrowers)} borrowers")

    print("")


def test_borrowing_api():

    print("Testing Borrowing API...")

    # First, create a book and borrower if they don't exist

    # Test borrowing a book
    borrow_data = {
        "borrower_id": 1,
        "book_id": 1,
        "borrow_date": "2023-01-01",
        "expected_return_date": "2023-01-15"
    }

    response = requests.post(f"{BASE_URL}/borrowing/rent", json=borrow_data)
    print(f"Borrow book response: {response.status_code}")
    if response.status_code == 201:
        borrowing = response.json()
        borrowing_id = borrowing["id"]
        print(f"Created borrowing record with ID: {borrowing_id}")

        # Test returning the book
        return_data = {
            "borrowing_id": borrowing_id,
            "actual_return_date": "2023-01-10"
        }

        response = requests.post(
            f"{BASE_URL}/borrowing/return", json=return_data)
        print(f"Return book response: {response.status_code}")
        if response.status_code == 200:
            print("Book returned successfully")

    print("")


if __name__ == "__main__":
    print("Running API tests...\n")

    try:
        test_book_api()
        test_borrower_api()
        test_borrowing_api()

        print("All tests completed!")
    except Exception as e:
        print(f"Error running tests: {e}")
