from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum, unique
from accountApp.database import db

@unique
class Role(Enum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"
    USER = "USER"


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    suspended = db.Column(db.Boolean, nullable=False)
 
    def __init__(self, email_address, username, password_hash, name, surname, role):
        self.email_address = email_address
        self.username = username
        self.password_hash = password_hash
        self.name = name
        self.surname = surname
        self.set_role(role) 
        self.suspended = False

    def set_role(self, role_str):
        role_mapping = {
            "ADMIN": Role.ADMIN,
            "EMPLOYEE": Role.EMPLOYEE,
            "USER": Role.USER
        }
        self.role = role_mapping.get(role_str, Role.USER)  # Default is USER


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    library = db.Column(ARRAY(db.String(50)))
    phone_number = db.Column(db.String(50))
    billing_address = db.Column(db.String(255))

    # Allows an easier access of the linked account attributes
    account = db.relationship('Account', lazy='select')