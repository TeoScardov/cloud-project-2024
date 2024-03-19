from flask import Flask
from flask_jwt_extended import JWTManager

from payment.config import Config


app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI

jwt = JWTManager(app)
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

from payment.views import blueprint
app.register_blueprint(blueprint, url_prefix='/api/payment')

app.run(port=8000, debug=True)


