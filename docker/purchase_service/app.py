import logging
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from sqlalchemy import true
from purchaseApp.database import db
from purchaseApp.config import *

def create_app(config_class="production"):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    app = Flask(__name__)
    app.config.from_object(get_config_map(config_class))
    
    from purchaseApp.views import blueprint
    app.register_blueprint(blueprint, url_prefix=Config.URL_PREFIX)

    if config_class == "production":
        JWTManager(app)
        CORS(app, origins="*")
        Swagger(app)
        
        db.init_app(app)
        with app.app_context():
            from purchaseApp import models
            db.create_all()
            
    return app

if __name__ == '__main__':
    app = create_app(config_class="development")
    app.run(debug=True)