from flask import Blueprint
from .model import load_users

users_blueprint = Blueprint('users', __name__)

users_db = load_users()

for u in users_db:
    print(u)
from . import routes
