from os import environ

class Config(object):
    """Base config."""
    DEBUG = False
    TESTING = False
    URL_PREFIX = environ.get("URL_PREFIX", '/api/payment/')
    SECRET_KEY = environ.get("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
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