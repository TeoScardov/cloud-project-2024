from flask import Flask
from flask_jwt_extended import JWTManager
import database
from accountApp.config import Config
from accountApp.routes import account

app = Flask(__name__)
app.register_blueprint(account, url_prefix='/api/account') 
app.config.from_object(Config)
jwt = JWTManager(app)
database.init_db(app)

if __name__ == '__main__':
    app.run(debug=True)
