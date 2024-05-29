from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from os import environ

try:
    URL_PREFIX = environ.get("URL_PREFIX")
    SECRET_KEY = environ.get("SECRET_KEY")
except Exception as e:
    print(f"Error: {e}", flush=True)
    print("Error reading environment variables", flush=True)
    exit(100)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

jwt = JWTManager(app)
CORS(app)

from paymentApp.views import blueprint
app.register_blueprint(blueprint, url_prefix=URL_PREFIX)