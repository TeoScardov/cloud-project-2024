class Config(object):
    """Base config."""
    JWT_SECRET_KEY = 'keyabc123456'
    #'postgresql://username:password@localhost/mydatabase'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin22@localhost/flask_db'
    JWT_TOKEN_TTL = 3600