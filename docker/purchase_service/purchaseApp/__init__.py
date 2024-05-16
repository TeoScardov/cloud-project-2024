from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")

jwt = JWTManager(app)
db = SQLAlchemy(app)
CORS(app)

from purchaseApp.views import blueprint
app.register_blueprint(blueprint, url_prefix='/api/purchase')

from purchaseApp import models
with app.app_context():
    db.create_all()