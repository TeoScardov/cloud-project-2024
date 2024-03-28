from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import account, model

# /api/account
@account.route('/')
def index():
    model.create_admin_account()
    return "Welcome to the account service API section."


@account.route('/register', methods=['POST'])
def register():
    # Parse JSON data sent with the request
    try:
        data = request.get_json()
    except:
        return jsonify({"message": "There was a problem with the json file."}), 400
    # Retrieve the JWT token, if present
    token = request.headers.get('Authorization', None)
    # Register the new account in the database
    message, code = model.register_account(data, token)
    return jsonify(message), code


@account.route('/login', methods=['POST'])
def login():
    # Parse JSON data sent with the request
    try:
        data = request.get_json()
    except:
        return jsonify({"message": "There was a problem with the json file."}), 400
    # Check login credentials, return the access token if the login is successful
    message, code = model.check_login_info(data)
    return jsonify(message), code


@account.route('/logout', methods=['POST'])
@jwt_required(fresh=True)
def logout():
    # To logout, discard the client-side token (to be implemented in the client-side app)
    return jsonify({"message": "Logged out."}), 200


@account.route('/update', methods=['POST'])
@jwt_required(fresh=True)
def update():
    # Parse JSON data sent with the request
    try:
        data = request.get_json()
    except:
        return jsonify({"message": "There was a problem with the json file."}), 400
    # Retrieve the JWT token
    token = request.headers.get('Authorization', None)
    # The info could be updated by the owner of the account, or by an admin
    message, code = model.update_info(token, data)
    return jsonify(message), code


@account.route('/authenticate', methods=['POST'])
@jwt_required()
def authenticate():
    # Retrieve the JWT token
    token = request.headers.get('Authorization', None)
    # Get the username and role associated to the JWT token
    message, code = model.authenticate_token(token)
    return jsonify(message), code