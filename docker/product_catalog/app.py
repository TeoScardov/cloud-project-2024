from urllib import request

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from os import environ
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://onlineshop:cloud2024@localhost/flask_db'

CORS(app)

db = SQLAlchemy(app)
class Book(db.Model):
    __tablename__ = 'books'

    isbn = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=False, nullable=False)
    publisher = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    price = db.Column(db.REAL)  # New column for price

    def json(self):
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher,
            'description': self.description,
            'price': self.price
        }

with app.app_context():
    db.create_all()

# test route
@app.route('/api/product/test', methods = ['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


@app.route('/api/product/create-book', methods=['POST'])
def create_book():
    try:
        data = request.get_json()

        # Check for empty fields
        if not all(field in data for field in ['isbn', 'title', 'author', 'publisher', 'description', 'price']):
            return make_response(jsonify({'message': 'All fields are required'}), 400)

        # Check for exceeding maximum length
        if len(data['isbn']) > 20 or len(data['title']) > 80 or len(data['author']) > 80 or len(
                data['publisher']) > 80 or len(data['description']) > 120:
            return make_response(jsonify({'message': 'Maximum length exceeded for one or more fields'}), 400)

        # Check for duplicate title
        existing_book = Book.query.filter_by(title=data['title']).first()
        if existing_book:
            return make_response(jsonify({'message': 'A book with this title already exists'}), 400)

        new_book = Book(isbn=data['isbn'], title=data['title'], author=data['author'], publisher=data['publisher'],
                        description=data['description'], price=data['price'])
        db.session.add(new_book)
        db.session.commit()
        return make_response(jsonify({'message': 'book created'}), 201)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({'message': 'Error: Duplicate ISBN or other integrity violation'}), 500)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating book: ' + str(e)}), 500)


# get all books
@app.route('/api/product/get-books', methods=['GET'])
def get_books():
    try:
        books = Book.query.all()
        return make_response(jsonify([book.json() for book in books]), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting books'}), 500)


# get a book by isbn
@app.route('/api/product/get-book-details', methods=['POST'])
def get_book_by_isbn():
    try:
        data = request.get_json()
        isbn = data.get('isbn')
        if isbn is None:
            return make_response(jsonify({'message': 'ISBN not provided in request body'}), 400)

        book = Book.query.get(isbn)
        if book:
            return make_response(jsonify({'book': book.json()}), 200)
        return make_response(jsonify({'message': 'book not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting book'}), 500)


@app.route('/api/product/update-book/<string:isbn>', methods=['PUT'])
def update_book(isbn):
    try:
        book = Book.query.get(isbn)
        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)

        data = request.get_json()

        # Check for exceeding maximum length
        if len(data.get('title', '')) > 80 or len(data.get('author', '')) > 80 or len(data.get('publisher', '')) > 80 or len(data.get('description', '')) > 120:
            return make_response(jsonify({'message': 'Maximum length exceeded for one or more fields'}), 400)

        # Check for duplicate title
        if 'title' in data and data['title'] != book.title:
            existing_book = Book.query.filter_by(title=data['title']).first()
            if existing_book:
                return make_response(jsonify({'message': 'A book with this title already exists'}), 400)

        # Update book attributes
        for key, value in data.items():
            setattr(book, key, value)

        db.session.commit()
        return make_response(jsonify({'message': 'Book updated'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error updating book: ' + str(e)}), 500)

# delete a book
@app.route('/api/product/delete-book/<string:isbn>', methods = ['DELETE'])
def delete_book(isbn):
    try:
        book = Book.query.get(isbn)
        if book:
            db.session.delete(book)
            db.session.commit()
            return make_response(jsonify({'message': 'book deleted'}),200)
        return make_response(jsonify({'message': 'book not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting book'}), 500)


if __name__ == '__main__':
    app.run(debug=True)


