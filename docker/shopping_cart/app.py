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


if __name__ == '__main__':
    app = create_app(config_class="development")
    app.run(debug=True)

