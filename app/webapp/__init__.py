from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'

    from .payment import payment_bp
    from .user import user_bp
    from .purchase import purchase_bp

    app.register_blueprint(payment_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(purchase_bp, url_prefix='/api')

    return app



