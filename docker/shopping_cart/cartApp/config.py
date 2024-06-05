"""Base config."""
JWT_SECRET_KEY = 'nyquist'
PRODUCT_SERVICE_URL = 'http://product_catalog:4000/api/product'
# PRODUCT_SERVICE_URL = 'http://127.0.0.1:5000/api/product'
USER_SERVICE_URL = 'http://account_management:4000/api/account'
# USER_SERVICE_URL = 'http://127.0.0.1:5001/api/account'
SWAGGER = {
    'title': 'Cart Service API',
    'uiversion': 3,
    'specs_route': '/api/docs/',
    'version': '1.0',
    'openapi': '3.0.2',
    'description': 'API for Cart Service',
}
# TESTING = False
TESTING = True
