import logging
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from accountApp.config import *
from accountApp.database import db
from accountApp.routes import account

def create_app(config_class="production"):
    if config_class != "production":
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    app = Flask(__name__)
    app.config.from_object(get_config_map(config_class))
    
    # Register Blueprints
    app.register_blueprint(account, url_prefix='/api/account')
    
    if config_class == "production":
        # Initialize extensions
        JWTManager(app)
        CORS(app)
        Swagger(app)

        # Initialize the database
        db.init_app(app)
        with app.app_context():
            db.create_all()
            from accountApp.dbmodel import create_admin_account
            create_admin_account()

    return app
    


if __name__ == '__main__':
    app = create_app(config_class="development")
    app.run(debug=True)