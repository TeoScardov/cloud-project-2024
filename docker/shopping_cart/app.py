import logging
from flask import Flask
from flask_jwt_extended import JWTManager
from cartApp.db import db
from cartApp.cart_controller import cart
from flask_cors import CORS
from flasgger import Swagger
from cartApp.config import *

def create_app(config_class="production"):
    if config_class != "production":
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    app = Flask(__name__)
    app.config.from_object(get_config_map(config_class))
          
    # Register Blueprints
    app.register_blueprint(cart, url_prefix='/api/cart')
    
    if config_class == "production":
        # Initialize extensions
        JWTManager(app)
        CORS(app)
        Swagger(app)
        
        # Initialize the database
        db.init_app(app)
        with app.app_context():
            db.create_all()
    
    return app
               
               
               
               
# app = Flask(__name__)
# app.register_blueprint(cart, url_prefix='/api/cart')
# app.config.from_pyfile('cartApp/config.py')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://onlineshop:cloud2024@localhost/flask_db'
# #app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
# #if app.config.get('TESTING'):
# #    app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://onlineshop:cloud2024@localhost/flask_db'

# db.init_app(app)
# CORS(app)
# swagger = Swagger(app)
# # Create the tables
# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    # app.run(port=5002, debug=True)


# Define a function to drop test tables
