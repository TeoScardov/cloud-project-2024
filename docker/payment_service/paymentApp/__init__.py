from flask import Flask
from flask_jwt_extended import JWTManager
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get("SECRET_KEY")

jwt = JWTManager(app)

from paymentApp.views import blueprint
app.register_blueprint(blueprint, url_prefix='/api/payment')