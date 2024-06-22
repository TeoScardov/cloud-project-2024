from flask import Blueprint, jsonify, make_response, request
from catalogApp.models import Book
from catalogApp.database import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func
from app import logging
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

blueprint = Blueprint('catalog', __name__)

# Test route
@blueprint.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

# Route to create a new book
@blueprint.route('/create-book', methods=['POST'])
def create_book():
    try:
        data = request.get_json()

        # Check for required fields
        required_fields = ['isbn', 'title', 'author', 'publisher', 'description', 'price']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({'message': 'All fields are required'}), 400)

        # Validate field lengths
        if len(data['isbn']) > 20 or len(data['title']) > 80 or len(data['author']) > 80 or len(data['publisher']) > 80 or len(data['description']) > 120:
            return make_response(jsonify({'message': 'Maximum length exceeded for one or more fields'}), 400)

        # Check if a book with the same title already exists
        existing_book = Book.query.filter_by(title=data['title']).first()
        if existing_book:
            return make_response(jsonify({'message': 'A book with this title already exists'}), 400)

        # Create a new book object
        new_book = Book(
            isbn=data['isbn'],
            title=data['title'],
            author=data['author'],
            publisher=data['publisher'],
            description=data['description'],
            price=data['price'],
            image_url=data.get('image_url')  # Handle optional image_url field
        )
        db.session.add(new_book)  # Add the new book to the session
        db.session.commit()  # Commit the session to save the book in the database
        return make_response(jsonify({'message': 'book created'}), 201)
    except IntegrityError:
        db.session.rollback()  # Rollback the session in case of an integrity error
        return make_response(jsonify({'message': 'Error: Duplicate ISBN or other integrity violation'}), 500)
    except Exception as e:
        logger.error(f"Error creating book: {e}")
        return make_response(jsonify({'message': f'error creating book: {str(e)}'}), 500)

# Route to get all books
@blueprint.route('/get-books', methods=['GET'])
def get_books():
    try:
        books = Book.query.all()  # Query all books
        return make_response(jsonify([book.json() for book in books]), 200)  # Return the list of books in JSON format
    except Exception as e:
        logger.error(f"Error getting books: {e}")
        return make_response(jsonify({'message': 'error getting books'}), 500)

# Route to get book details by ISBN
@blueprint.route('/get-book-details', methods=['POST'])
def get_book_by_isbn():
    try:
        data = request.get_json()
        isbn = data.get('isbn')
        if not isbn:
            return make_response(jsonify({'message': 'ISBN not provided in request body'}), 400)

        with Session(db.engine) as session:
            book = session.get(Book, isbn)  # Query the book by ISBN using Session.get()

        if book:
            return make_response(jsonify({'book': book.json()}), 200)
        return make_response(jsonify({'message': 'book not found'}), 404)
    except Exception as e:
        logger.error(f"Error getting book details: {e}")
        return make_response(jsonify({'message': 'error getting book'}), 500)

# Route to update a book by ISBN
@blueprint.route('/update-book/<string:isbn>', methods=['PUT'])
def update_book(isbn):
    try:
        with Session(db.engine) as session:
            book = session.get(Book, isbn)  # Use Session.get()
            if not book:
                return make_response(jsonify({'message': 'Book not found'}), 404)

            data = request.get_json()

            # Validate field lengths
            if len(data.get('title', '')) > 80 or len(data.get('author', '')) > 80 or len(data.get('publisher', '')) > 80 or len(data.get('description', '')) > 120:
                return make_response(jsonify({'message': 'Maximum length exceeded for one or more fields'}), 400)

            # Check if a book with the new title already exists
            if 'title' in data and data['title'] != book.title:
                existing_book = session.query(Book).filter_by(title=data['title']).first()
                if existing_book:
                    return make_response(jsonify({'message': 'A book with this title already exists'}), 400)

            # Update book attributes
            for key, value in data.items():
                setattr(book, key, value)

            session.commit()  # Commit the session to save the changes
        return make_response(jsonify({'message': 'Book updated'}), 200)
    except Exception as e:
        logger.error(f"Error updating book: {e}")
        return make_response(jsonify({'message': f'Error updating book: {str(e)}'}), 500)

# Route to delete a book by ISBN
@blueprint.route('/delete-book/<string:isbn>', methods=['DELETE'])
def delete_book(isbn):
    try:
        with Session(db.engine) as session:
            book = session.get(Book, isbn)  # Use Session.get()
            if book:
                session.delete(book)  # Delete the book
                session.commit()  # Commit the session to save the changes
                return make_response(jsonify({'message': 'book deleted'}), 200)
            return make_response(jsonify({'message': 'book not found'}), 404)
    except Exception as e:
        logger.error(f"Error deleting book: {e}")
        return make_response(jsonify({'message': f'error deleting book: {str(e)}'}), 500)

# Route to get random books
@blueprint.route('/get-random-books/<int:number>', methods=['GET'])
def get_random_books(number):
    try:
        random_books = Book.query.order_by(func.random()).limit(number).all()  # Query 5 random books
        return make_response(jsonify([book.json() for book in random_books]), 200)
    except Exception as e:
        logger.error(f"Error getting random books: {e}")
        return make_response(jsonify({'message': 'error getting random books'}), 500)

