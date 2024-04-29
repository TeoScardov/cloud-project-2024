"""Base config."""
JWT_SECRET_KEY = 'nyquist'
# DATABASE_URI = 'jdbc:sqlite:identifier.sqlite'
DATABASE_URI = 'jdbc:postgresql://0.0.0.0:5432/flask_db'
PRODUCT_SERVICE_URL = 'http://127.0.0.1:4004'
USER_SERVICE_URL = 'http://127.0.0.1:4001'
