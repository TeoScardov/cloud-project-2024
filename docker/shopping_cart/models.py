from datetime import datetime
from .db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    total = db.Column(db.REAL, nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    exp_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    items = db.relationship('CartItem', backref='cart', lazy=True)

    def __init__(self, total=None, user_id=None, items=[], exp_date=None):
        self.id = str(uuid.uuid4())
        self.total = total
        self.user_id = user_id
        self.items = items
        if exp_date is not None:
            self.exp_date = exp_date


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.REAL, nullable=False)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)

    def __init__(self, name, price):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price


class CartItem(db.Model):
    __tablename__ = 'cart_item'

    cart_id = db.Column(UUID(as_uuid=True), db.ForeignKey('cart.id'), primary_key=True)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(255), nullable=False, default="")
    price = db.Column(db.REAL, nullable=False, default=0.0)

    def __init__(self, cart_id=None, product_id=None, quantity=0, name="", price=0.0):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.name = name
        self.price = price



