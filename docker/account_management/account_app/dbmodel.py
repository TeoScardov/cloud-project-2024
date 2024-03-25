from enum import Enum, unique
from account_app.database import db

@unique
class Role(Enum):
    ADMIN = "Admin"
    EMPLOYEE = "Employee"
    USER = "User"

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    suspended = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
        
    def __init__(self, username, password_hash, role, name, surname, suspended=False):
        self.username = username
        self.password_hash = password_hash
        self.set_role(role) 
        self.suspended = suspended
        self.name = name
        self.surname = surname

    def set_role(self, role_str):
        role_mapping = {
            "Admin": Role.ADMIN,
            "Employee": Role.EMPLOYEE,
            "User": Role.USER
        }
        self.role = role_mapping.get(role_str, Role.USER)  # Default to USER