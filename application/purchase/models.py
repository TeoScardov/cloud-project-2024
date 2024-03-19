from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

class PurchaseDao(db.Model):
    __tablename__ = 'orders'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    #account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('account.id'), nullable=False)
    account_id = db.Column(UUID(as_uuid=True), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('PENDING', 'APPROVED', 'REJECTED', name='status_enum'), nullable=False)

    def __init__(self, account_id, total_price, status):
        self.id = str(uuid.uuid4())
        self.account_id = account_id
        self.order_date = db.func.current_timestamp()
        self.total_price = total_price
        self.status = status

    def __repr__(self):
        return f'<Purchase {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'order_date': self.order_date,
            'total_price': self.total_price,
            'status': self.status
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return PurchaseDao.query.all()
    
    @staticmethod
    def get_by_id(id):
        return PurchaseDao.query.get(id)
    
    
class PurchaseItemDao(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    #order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id'), nullable=False)
    #book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('book.id'), nullable=False)
    order_id = db.Column(UUID(as_uuid=True), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), nullable=False)

    def __init__(self, order_id, product_id):
        self.id = str(uuid.uuid4())
        self.order_id = order_id
        self.product_id = product_id

    def __repr__(self):
        return f'<PurchaseItem {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return PurchaseItemDao.query.all()
    
    @staticmethod
    def get_by_id(id):
        return PurchaseItemDao.query.get(id)
    
    @staticmethod
    def get_by_order_id(order_id):
        return PurchaseItemDao.query.filter_by(order_id=order_id).all()

class PaymentDao(db.Model):
    __tablename__ = 'payment'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    #purchase_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    purchase_id = db.Column(UUID(as_uuid=True), nullable=False)

    def __init__(self, purchase_id):
        self.id = str(uuid.uuid4())
        self.purchase_id = purchase_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'purchase_id': self.purchase_id
        }
    
    @staticmethod
    def get_by_id(payment_id):
        return PaymentDao.query.filter_by(id=payment_id).first()

    @staticmethod
    def get_by_purchase_id(purchase_id):
        return PaymentDao.query.filter_by(purchase_id=purchase_id).first()