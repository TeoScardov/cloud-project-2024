import uuid
from purchaseApp.database import db
from sqlalchemy.dialects.postgresql import UUID

class PurchaseDao(db.Model):
    """
    A class used to represent a Purchase

    Attributes
    ----------
    id : str
        a unique identifier for the purchase
    account_id : str
        a unique identifier for the account
    order_date : datetime
        the date of the purchase
    total: float
        the total price of the purchase
    status : str
        the status of the purchase

    Methods
    -------
    to_dict()
        Returns a dictionary representation of the purchase
    save()
        Saves the purchase to the database
    delete()
        Deletes the purchase from the database
    get_all()
        Returns all purchases in the database
    get_by_id(id)   
        Returns the purchase with the given id
    """

    __tablename__ = 'orders'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    account_id = db.Column(UUID(as_uuid=True), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('PENDING', 'APPROVED', 'REJECTED', name='status_enum'), nullable=False)

    def __init__(self, account_id, total, status):
        """
        Parameters
        ----------
        id : str
            a unique identifier for the purchase
        account_id : str
            a unique identifier for the account
        order_date : datetime
            the date of the purchase
        total : float
            the total price of the purchase
        status : str
            the status of the purchase
        """

        self.id = uuid.uuid4()
        self.account_id = account_id
        self.order_date = db.func.current_timestamp()
        self.total = total
        self.status = status

    def __repr__(self):
        return f'<Purchase {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'order_date': self.order_date,
            'total': self.total,
            'status': self.status
        }
    
    def save(self):
        """
        Saves the purchase to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deletes the purchase from the database
        """
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        """
        Rolls back the transaction
        """
        db.session.rollback()

    @staticmethod
    def get_all():
        """
        Returns all purchases in the database
        """
        return PurchaseDao.query.all()
    
    @staticmethod
    def get_by_id(id):
        """
        Returns the purchase with the given id
        """
        return PurchaseDao.query.get(id)

    @staticmethod
    def get_by_account_id(account_id):
        """
        Returns all purchases with the given account id
        """
        return PurchaseDao.query.filter_by(account_id=account_id).all()
    
    
class PurchaseItemDao(db.Model):
    """
    A class used to represent a Purchase Item

    Attributes
    ----------
    id : str
        a unique identifier for the purchase item
    order_id : str
        a unique identifier for the order (foreign key)
    product_id : str
        a unique identifier for the product

    Methods
    -------
    to_dict()
        Returns a dictionary representation of the purchase item
    save()
        Saves the purchase item to the database
    delete()
        Deletes the purchase item from the database
    get_all()
        Returns all purchase items in the database
    get_by_id(id)
        Returns the purchase item with the given id
    get_by_order_id(order_id)
        Returns all purchase items with the given order id
    """

    __tablename__ = 'order_items'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id'), nullable=False, unique=True)
    product_id = db.Column(db.JSON, nullable=False)

    def __init__(self, order_id, product_id):
        """
        Parameters
        ----------
        id : str
            a unique identifier for the purchase item

        order_id : str
            a unique identifier for the order

        product_id : str
            a unique identifier for the product
        """
        #self.id = str(uuid.uuid4())
        self.id = uuid.uuid4()
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
        """
        Saves the purchase item to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deletes the purchase item from the database
        """
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        """
        Rolls back the transaction
        """
        db.session.rollback()

    @staticmethod
    def get_all():
        """
        Returns all purchase items in the database
        """
        return PurchaseItemDao.query.all()
    
    @staticmethod
    def get_by_id(id):
        """
        Returns the purchase item with the given id
        """
        return PurchaseItemDao.query.get(id)
    
    @staticmethod
    def get_by_order_id(order_id):
        """
        Returns all purchase items with the given order id
        """
        return PurchaseItemDao.query.filter_by(order_id=order_id).one_or_none()

class PaymentDao(db.Model):
    """
    A class used to represent a Payment

    Attributes
    ----------
    id : str
        a unique identifier for the payment
    purchase_id : str
        a unique identifier for the purchase (foreign key)

    Methods
    -------
    to_dict()
        Returns a dictionary representation of the payment
    save()
        Saves the payment to the database
    get_by_id(payment_id)
        Returns the payment with the given id
    get_by_purchase_id(purchase_id)
        Returns the payment with the given purchase id
    """

    __tablename__ = 'payment'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    purchase_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id'), nullable=False, unique=True)

    def __init__(self, purchase_id):
        """
        Parameters
        ----------
        id : str
            a unique identifier for the payment
        purchase_id : str
            a unique identifier for the purchase
        """
        self.id = uuid.uuid4()
        self.purchase_id = purchase_id

    def save(self):
        """
        Saves the payment to the database
        """
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """
        Deletes the payment from the database
        """
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        """
        Rolls back the transaction
        """
        db.session.rollback()

    def to_dict(self):
        return {
            'id': self.id,
            'purchase_id': self.purchase_id
        }
    
    @staticmethod
    def get_by_id(payment_id):
        """
        Returns the payment with the given id
        """
        return PaymentDao.query.filter_by(id=payment_id).first()

    @staticmethod
    def get_by_purchase_id(purchase_id):
        """
        Returns the payment with the given purchase id
        """
        return PaymentDao.query.filter_by(purchase_id=purchase_id).first()