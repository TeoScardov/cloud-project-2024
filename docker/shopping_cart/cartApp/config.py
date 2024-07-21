from os import environ

PRODUCT_SERVICE_URL = environ.get("PRODUCT_CATALOG_URL", 'http://product_catalog:4003/api/product') 
USER_SERVICE_URL = environ.get("USER_SERVICE_URL", 'http://account_management:4001/api/account') 
class Config(object):
    """Base config."""
    DEBUG = False
    TESTING = False
    URL_PREFIX = environ.get("URL_PREFIX", '/api/cart')
    SECRET_KEY = environ.get("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = environ.get("DB_URL")
    SWAGGER = {
        'title': 'Purchase Service API',
        'uiversion': 3,
        'specs_route': '/api/docs/',
        'version': '1.0',
        'description': 'API for Purchase Service',
    }
        
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

def get_config_map(name):
    config_map = {
        'production': Config,
        'development': DevelopmentConfig,
        'testing': TestingConfig
    }

    return config_map[name]

