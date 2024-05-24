from sqlalchemy.dialects.postgresql import ARRAY, UUID, JSONB
from enum import Enum, unique
import uuid
from werkzeug.security import generate_password_hash
from accountApp.config import Config
from accountApp.database import db


@unique
class Role(Enum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"
    USER = "USER"



class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_address = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    suspended = db.Column(db.Boolean, nullable=False, default=False)
 
    def __init__(self, email_address, username, password_hash, name, surname, role):
        self.email_address = email_address
        self.username = username
        self.password_hash = password_hash
        self.name = name
        self.surname = surname
        self.set_role(role) 

    def set_role(self, role_str):
        role_mapping = {
            "ADMIN": Role.ADMIN,
            "EMPLOYEE": Role.EMPLOYEE,
            "USER": Role.USER
        }
        self.role = role_mapping.get(role_str, Role.USER)  # Default is USER



class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('accounts.id'), unique=True, nullable=False)
    library = db.Column(ARRAY(db.String(50)))
    phone_number = db.Column(db.String(50))
    billing_address = db.Column(db.String(255))
    credit_card_info = db.Column(JSONB)



def create_admin_account():
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
        print(f"Error creating admin account: {e}")