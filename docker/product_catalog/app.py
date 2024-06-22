import logging
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from catalogApp.config import *
from catalogApp.database import db

def create_app(config_class="production"):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    app = Flask(__name__)
    app.config.from_object(get_config_map(config_class))
    
    from catalogApp.views import blueprint
    app.register_blueprint(blueprint, url_prefix=Config.URL_PREFIX)

    if config_class == "production":
        JWTManager(app)
        CORS(app)
        Swagger(app)
        
        db.init_app(app)
        with app.app_context():
            from catalogApp import models
            db.create_all()
            
    return app

if __name__ == '__main__':
    app = create_app(config_class="development")
    app.run(debug=True)




