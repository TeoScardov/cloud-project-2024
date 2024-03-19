from flask import Flask
from flask_jwt_extended import JWTManager

from views import user_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


jwt = JWTManager(app)


app.register_blueprint(user_bp, url_prefix='/api/user')

app.run(port=8002, debug=True)
