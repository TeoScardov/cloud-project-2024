from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'

    from .Payment.payment import payment_bp
    from .User.user import user_bp
    from .Purchase.purchase import purchase_bp

    app.register_blueprint(payment_bp, url_prefix='/api/payment')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(purchase_bp, url_prefix='/api/purchase')

    return app



