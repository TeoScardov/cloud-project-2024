from flask import Flask
from users.routes import users_blueprint
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.register_blueprint(users_blueprint, url_prefix='/users')
app.config['JWT_SECRET_KEY'] = 'key999'  
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
