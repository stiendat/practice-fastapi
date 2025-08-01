# Test Data

This directory contains sample data for testing the Library Management System.

## Files

### books.csv
Sample book data in CSV format for importing into the database.

**Format**: Semicolon-separated values with the following columns:
- ISBN: International Standard Book Number
- Book-Title: Title of the book
- Book-Author: Author name
- Year-Of-Publication: Publication year
- Publisher: Publishing house
- Image-URL-S: Small cover image URL
- Image-URL-M: Medium cover image URL  
- Image-URL-L: Large cover image URL

**Usage**:
```bash
# Import sample data (Docker environment)
docker-compose exec web python import_books.py --clear

# Or using Makefile
make import-books
```

## Adding Your Own Data

You can replace `books.csv` with your own book data following the same format, or specify a different file:

```bash
docker-compose exec web python import_books.py --csv-file path/to/your/books.csv
```
