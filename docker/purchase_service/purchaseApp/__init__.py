from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from os import environ

try:
    URL_PREFIX = environ.get("URL_PREFIX")
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
except Exception as e:
    print(f"Error: {e}", flush=True)
    print("Error reading environment variables", flush=True)
    exit(100)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

jwt = JWTManager(app)
db = SQLAlchemy(app)
CORS(app)

from purchaseApp.views import blueprint
app.register_blueprint(blueprint, url_prefix=URL_PREFIX)

from purchaseApp import models
with app.app_context():
    db.create_all()