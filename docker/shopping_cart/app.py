from flask import Flask
from .db import db
from .cart_controller import cart
from os import environ

app = Flask(__name__)
app.register_blueprint(cart, url_prefix='/api/cart')
app.config.from_pyfile('config.py')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///identifier.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://onlineshop:cloud2024@localhost/flask_db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db.init_app(app)

# Create the tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
