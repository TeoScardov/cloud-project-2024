import os

class Config(object):
    """Base config."""
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'keyabc123456')
    #'postgresql://username:password@localhost/mydatabase'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_TOKEN_TTL = int(os.getenv('JWT_TOKEN_TTL', '3600'))
    ADMIN_PASSWORD = "cloud2024"