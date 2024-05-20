from flask import Flask
from cartApp.db import db
from cartApp.cart_controller import cart
from os import environ
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(cart, url_prefix='/api/cart')
app.config.from_pyfile('cartApp/config.py')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///identifier.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://onlineshop:cloud2024@localhost/flask_db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db.init_app(app)
CORS(app)
swagger = Swagger(app)
# Create the tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(port=5002, debug=True)
