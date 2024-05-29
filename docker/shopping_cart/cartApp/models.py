import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from .db import db


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    total = db.Column(db.REAL, nullable=True)
    user_id = db.Column(db.String(255), nullable=True)
    exp_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')

    def __init__(self, total=None, user_id=None, items=[], exp_date=None):
        self.id = str(uuid.uuid4())
        self.total = total
        self.user_id = user_id
        self.items = items
        if exp_date is not None:
            self.exp_date = exp_date



class CartItem(db.Model):
    __tablename__ = 'cart_item'

    cart_id = db.Column(UUID(as_uuid=True), db.ForeignKey('cart.id'), primary_key=True)
    isbn = db.Column(db.String(20), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    title = db.Column(db.String(255), nullable=False, default="")
    price = db.Column(db.REAL, nullable=False, default=0.0)

    def __init__(self, cart_id=None, isbn=None, quantity=0, title="", price=0.0):
        self.cart_id = cart_id
        self.isbn = isbn
        self.quantity = quantity
        self.title = title
        self.price = price



