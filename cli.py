from typer import Typer
import requests
import json
from commands.init_database.main import init_database
from settings import BASE_URL

app = Typer()

@app.command("init_database")
def cmd_init_database():
    print("Initializing database")
    init_database()


@app.command("import_books")
def cmd_import_books():
    """Import books from CSV file"""
    print("Importing books from CSV...")
    try:
        from scripts.import_books import main as import_main
        import_main()
    except Exception as e:
        print(f"Failed to import books: {str(e)}")


@app.command("create_tables")
def cmd_create_tables():
    """Create database tables"""
    print("Creating database tables...")
    try:
        from src.models.library_models import create_tables
        create_tables()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Failed to create tables: {str(e)}")


@app.command("run_test")
def cmd_run_test():
    print("🧪 Testing Library Management System API...")
    
    try:
        # Test root endpoint
        print("\n1️⃣ Testing root endpoint...")
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test health endpoint
        print("\n2️⃣ Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test books API
        print("\n3️⃣ Testing books API...")
        response = requests.get(f"{BASE_URL}/api/v1/books/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total books: {data.get('total', 'N/A')}")
            books = data.get('books', [])
            if books:
                print(f"First book: {books[0].get('title', 'N/A')} by {books[0].get('author', 'N/A')}")
        
        # Test users API
        print("\n4️⃣ Testing users API...")
        response = requests.get(f"{BASE_URL}/api/v1/users/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total users: {data.get('total', 'N/A')}")
        
        # Test creating a user
        print("\n5️⃣ Testing create user...")
        user_data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone_number": "0123456789",
            "address": "123 Test Street"
        }
        response = requests.post(f"{BASE_URL}/api/v1/users/", json=user_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            user = response.json()
            user_id = user['id']
            print(f"Created user: {user['full_name']} (ID: {user_id})")
            
            # Test rental
            print("\n6️⃣ Testing create rental...")
            rental_response = requests.post(
                f"{BASE_URL}/api/v1/rentals/rent-simple?user_id={user_id}&book_id=1&days=14"
            )
            print(f"Status: {rental_response.status_code}")
            if rental_response.status_code == 201:
                rental = rental_response.json()
                rental_id = rental['id']
                print(f"Created rental: ID {rental_id}")
                
                # Test return book
                print("\n7️⃣ Testing return book...")
                return_data = {"notes": "Book returned in good condition"}
                return_response = requests.post(
                    f"{BASE_URL}/api/v1/rentals/{rental_id}/return",
                    json=return_data
                )
                print(f"Status: {return_response.status_code}")
                if return_response.status_code == 200:
                    returned = return_response.json()
                    print(f"Book returned successfully: {returned['status']}")
        
        print("\n✅ API tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")


if __name__ == "__main__":
    app()
