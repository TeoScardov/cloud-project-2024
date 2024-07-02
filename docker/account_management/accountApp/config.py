import os

class Config(object):
    """Base config."""
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'keyabc123456')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_TOKEN_TTL = int(os.getenv('JWT_TOKEN_TTL', '3600'))
    ADMIN_PASSWORD = "cloud2024"
    SWAGGER = {
        'title': 'Account Management Service API',
        'uiversion': 3,
        'specs_route': '/api/docs/',
        'version': '1.0',
        'description': 'API for Account Service',
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