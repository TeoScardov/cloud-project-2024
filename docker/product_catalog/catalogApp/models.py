from catalogApp.database import db

class Book(db.Model):
    __tablename__ = 'books'

    isbn = db.Column(db.String(20), primary_key=True)  # ISBN as the primary key
    title = db.Column(db.String(80), unique=True, nullable=False)  # Title of the book
    author = db.Column(db.String(80), nullable=False)  # Author of the book
    publisher = db.Column(db.String(80), nullable=False)  # Publisher of the book
    description = db.Column(db.String(120), nullable=False)  # Description of the book
    price = db.Column(db.REAL)  # Price of the book
    image_url = db.Column(db.String(255))  # URL of the book image
    
    def __init__(self, isbn, title, author, publisher, description, price, image_url=None):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.description = description
        self.price = price
        self.image_url = image_url

    # Method to convert a book object to JSON
    def json(self):
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url  # Include image URL in JSON response
        }