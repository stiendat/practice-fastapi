#!/usr/bin/env python3
"""
Simple test to check if our database models work
"""
import sqlite3
import json

def test_books_simple():
    """Test reading books directly from SQLite"""
    try:
        conn = sqlite3.connect('library.db')
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, title, author, year, quantity FROM books LIMIT 5")
        books = cursor.fetchall()
        
        books_list = []
        for book in books:
            books_list.append({
                "id": book["id"],
                "title": book["title"], 
                "author": book["author"],
                "year": book["year"],
                "quantity": book["quantity"]
            })
        
        conn.close()
        return books_list
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    print("🧪 Testing Direct Database Access")
    books = test_books_simple()
    
    if books:
        print(f"✅ Found {len(books)} books:")
        for book in books:
            print(f"   📚 {book['title']} by {book['author']} ({book['year']}) - Qty: {book['quantity']}")
        
        print(f"\n📋 JSON Response:")
        print(json.dumps(books, indent=2))
    else:
        print("❌ No books found")

if __name__ == "__main__":
    main()