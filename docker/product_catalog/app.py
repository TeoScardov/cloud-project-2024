from urllib import request

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@flask_db:5432/postgres'

db = SQLAlchemy(app)
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=True, nullable=False)
    publisher = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'title': self.title, 'author': self.author, 'publisher': self.publisher, 'description': self.description}

with app.app_context():
    db.create_all()

# test route
@app.route('/test', methods = ['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

# create a book
@app.route('/books', methods=['POST'])
def create_book():
    try:
        data = request.get_json()
        new_book = Book(title =data['title'], author = data['author'], publisher = data['publisher'], description =data['description'])
        db.session.add(new_book)
        db.session.commit()
        return make_response(jsonify({'message':'book created'}), 201)
    except Exception as e:
     return make_response(jsonify({'message': 'error creating book'}),500)


# get all books
@app.route('/books', methods=['GET'])
def get_books():
    try:
        books = Book.query.all()
        return make_response(jsonify([book.json() for book in books]), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting books'}), 500)

# get a book by id
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    try:
        book = Book.query.filter_by(id = id).first()
        if book:
            return make_response(jsonify({'book': book.json()}), 200)
        return make_response(jsonify({'message': 'book not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting book'}),500)

# update a book
@app.route('/books/<int:id>', methods = ['PUT'])
def update_book(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            data = request.get_json()
            book.title = data['title']
            book.author = data['author']
            book.publisher = data['publisher']
            book.description = data['description']
            db.session.commit()
            return make_response(jsonify({'message': 'book updated'}), 200)
        return make_response(jsonify({'message': 'book not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating book'}), 500)

# delete a book
@app.route('/books/<int:id>', methods = ['DELETE'])
def delete_book(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return make_response(jsonify({'message': 'book deleted'}),200)
        return make_response(jsonify({'message': 'book not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting book'}), 500)
