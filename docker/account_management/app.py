from flask import Flask
from flask_jwt_extended import JWTManager
from account_app.config import Config
from account_app.database import db
from account_app.routes import account

app = Flask(__name__)
app.register_blueprint(account, url_prefix='/api/account') 
app.config.from_object(Config)

jwt = JWTManager(app)

db.init_app(app)
# Create the tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)