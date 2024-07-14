from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, JSON
import uuid, logging
from accountApp.database import db

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID as string
    email_address = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="USER")
    suspended = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email_address, username, password_hash, name, surname, role):
        self.email_address = email_address
        self.username = username
        self.password_hash = password_hash
        self.name = name
        self.surname = surname
        self.set_role(role)

    def set_role(self, role_str):
        if role_str in ["USER", "EMPLOYEE", "ADMIN"]:
            self.role = role_str
        else:
            self.role = "USER"

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = db.Column(db.String(36), db.ForeignKey('accounts.id'), unique=True, nullable=False)
    library = db.Column(db.JSON)
    phone_number = db.Column(db.String(50))
    billing_address = db.Column(db.String(255))
    cc = db.Column(db.String(50))
    expiredate = db.Column(db.String(50))
    cvv = db.Column(db.String(50))

    def set_library(self, book_list):
        self.library = book_list

    def get_library(self):
        return self.library if self.library else []



def create_admin_account():
    from werkzeug.security import generate_password_hash
    from accountApp.config import Config
    try:
        if not Account.query.filter_by(username='admin1').first():
            admin_account = Account(
                email_address='admin@example.com',
                username='admin1',
                password_hash=generate_password_hash(Config.ADMIN_PASSWORD),
                name='Admin',
                surname='User',
                role='ADMIN'
            )
            db.session.add(admin_account)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.getLogger().error(f"Error creating admin account: {e}")