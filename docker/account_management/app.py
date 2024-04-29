from flask import Flask
from flask_jwt_extended import JWTManager
from accountApp.config import Config
from accountApp.database import db
from accountApp.routes import account

app = Flask(__name__)
app.register_blueprint(account, url_prefix='/api/account') 
app.config.from_object(Config)

jwt = JWTManager(app)

db.init_app(app)
# Create the tables
with app.app_context():
    db.create_all()
    
    from accountApp.dbmodel import create_admin_account
    create_admin_account()

if __name__ == '__main__':
    app.run(debug=True)