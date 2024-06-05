import pytest
import json
import os

# Set the DB_URL environment variable before importing the app
os.environ['DB_URL'] = 'sqlite:///:memory:'

# Import the Flask app and database from the code above
from app import app, db, Book

# allows to make requests to application as you were an external client without actually running the server
@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    #configures the app to use an in-memory SQLite db. This ensures that the test runs in isolation
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as testing_client:
        with app.app_context(): #push an application context
            db.create_all() #create db tables
            yield testing_client #testing happening
            db.drop_all() #drop tables


# test creation of a book
def test_create_book_success(test_client):
    new_book_data = {
        "isbn": "1234567890123",
        "title": "Test Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "description": "This is a test book",
        "price": 19.99,
        "image_url": "http://example.com/testbook.jpg"
    }

    response = test_client.post('/api/product/create-book', data=json.dumps(new_book_data), content_type='application/json')
    assert response.status_code == 201
    assert response.json['message'] == 'book created'

# test missing fields during creation
def test_create_book_missing_fields(test_client):
    incomplete_book_data = {
        "isbn": "1234567890123",
        "title": "Test Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "description": "This is a test book"
    }

    response = test_client.post('/api/product/create-book', data=json.dumps(incomplete_book_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'All fields are required'

# test duplicate titles
def test_create_book_duplicate_title(test_client):
    book_data_1 = {
        "isbn": "1234567890123",
        "title": "Test Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "description": "This is a test book",
        "price": 19.99,
        "image_url": "http://example.com/testbook.jpg"
    }

    book_data_2 = {
        "isbn": "9876543210987",
        "title": "Test Book",
        "author": "Another Author",
        "publisher": "Another Publisher",
        "description": "This is another test book",
        "price": 29.99,
        "image_url": "http://example.com/anothertestbook.jpg"
    }

    test_client.post('/api/product/create-book', data=json.dumps(book_data_1), content_type='application/json')
    response = test_client.post('/api/product/create-book', data=json.dumps(book_data_2), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'A book with this title already exists'

# test long fields
def test_create_book_long_fields(test_client):
    long_fields_data = {
        "isbn": "123456789012345678901",
        "title": "T" * 81,
        "author": "A" * 81,
        "publisher": "P" * 81,
        "description": "D" * 121,
        "price": 19.99,
        "image_url": "http://example.com/testbook.jpg"
    }

    response = test_client.post('/api/product/create-book', data=json.dumps(long_fields_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'Maximum length exceeded for one or more fields'

# Test getting all books
def test_get_books(test_client):
    response = test_client.get('/api/product/get-books')
    assert response.status_code == 200
    assert isinstance(response.json, list)


# Test getting book details by ISBN
def test_get_book_by_isbn(test_client):
    # First, create a book to fetch
    new_book_data = {
        "isbn": "9876543210984",
        "title": "Fetch Test Book",
        "author": "Fetch Test Author",
        "publisher": "Fetch Test Publisher",
        "description": "This is a fetch test book",
        "price": 19.99,
        "image_url": "http://example.com/fetchtestbook.jpg"
    }

    test_client.post('/api/product/create-book', data=json.dumps(new_book_data), content_type='application/json')

    # Fetch the created book by ISBN
    response = test_client.post('/api/product/get-book-details', data=json.dumps({"isbn": "9876543210984"}), content_type='application/json')
    assert response.status_code == 200
    assert response.json['book']['title'] == 'Fetch Test Book'

# Test getting book details with missing ISBN
def test_get_book_by_isbn_missing(test_client):
    response = test_client.post('/api/product/get-book-details', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'ISBN not provided in request body'


# Test updating a book
def test_update_book(test_client):
    # First, create a book to update
    new_book_data = {
        "isbn": "1234567890123",
        "title": "Update Test Book",
        "author": "Update Test Author",
        "publisher": "Update Test Publisher",
        "description": "This is an update test book",
        "price": 19.99,
        "image_url": "http://example.com/updatetestbook.jpg"
    }

    test_client.post('/api/product/create-book', data=json.dumps(new_book_data), content_type='application/json')

    # Update the book
    update_data = {
        "title": "Updated Test Book",
        "author": "Updated Test Author"
    }

    response = test_client.put('/api/product/update-book/1234567890123', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'] == 'Book updated'


# Test updating a non-existent book
def test_update_nonexistent_book(test_client):
    update_data = {
        "title": "Nonexistent Book",
        "author": "Nonexistent Author"
    }

    response = test_client.put('/api/product/update-book/0000000000000', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 404
    assert response.json['message'] == 'Book not found'

# Test deleting a book
def test_delete_book(test_client):
    # First, create a book to delete
    new_book_data = {
        "isbn": "1234567890123",
        "title": "Delete Test Book",
        "author": "Delete Test Author",
        "publisher": "Delete Test Publisher",
        "description": "This is a delete test book",
        "price": 19.99,
        "image_url": "http://example.com/deletetestbook.jpg"
    }

    test_client.post('/api/product/create-book', data=json.dumps(new_book_data), content_type='application/json')

    # Delete the book
    response = test_client.delete('/api/product/delete-book/1234567890123')
    assert response.status_code == 200
    assert response.json['message'] == 'book deleted'

# Test deleting a non-existent book
def test_delete_nonexistent_book(test_client):
    response = test_client.delete('/api/product/delete-book/0000000000000')
    assert response.status_code == 404
    assert response.json['message'] == 'book not found'

# test getting random books
@pytest.fixture
def test_client():
    with app.test_client() as client:
        with app.app_context():
            # Create all tables
            db.create_all()
            yield client
            # Drop all tables
            db.drop_all()

def add_books_to_db():
    books = [
        Book(isbn="1111111111111", title="Book One", author="Author One", publisher="Publisher One", description="Description One", price=10.99, image_url="http://example.com/book1.jpg"),
        Book(isbn="2222222222222", title="Book Two", author="Author Two", publisher="Publisher Two", description="Description Two", price=12.99, image_url="http://example.com/book2.jpg"),
        Book(isbn="3333333333333", title="Book Three", author="Author Three", publisher="Publisher Three", description="Description Three", price=15.99, image_url="http://example.com/book3.jpg"),
        Book(isbn="4444444444444", title="Book Four", author="Author Four", publisher="Publisher Four", description="Description Four", price=9.99, image_url="http://example.com/book4.jpg"),
        Book(isbn="5555555555555", title="Book Five", author="Author Five", publisher="Publisher Five", description="Description Five", price=8.99, image_url="http://example.com/book5.jpg"),
    ]
    for book in books:
        db.session.add(book)
    db.session.commit()

def test_get_random_books(test_client):
    with app.app_context():
        add_books_to_db()

    response = test_client.get('/api/product/get-random-books/3')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 3  # Check if 3 books are returned
    assert all('isbn' in book for book in data)  # Check if 'isbn' is present in all returned books

    # Repeat to check for randomness
    response2 = test_client.get('/api/product/get-random-books/3')
    data2 = response2.get_json()
    assert len(data2) == 3
    assert data != data2  # There should be some difference between the two sets of random books