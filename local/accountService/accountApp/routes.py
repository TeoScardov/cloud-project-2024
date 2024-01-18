from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import account, model

@account.route('/')
def index():
    return "Welcome to the account service API section."


@account.route('/login', methods=['POST'])
def login():
    # Parse JSON data sent with the request
    data = request.get_json()
    # Check login credentials
    token = model.check_login_info(data)
    if token is not None:
        return jsonify({"message": "Login succesful", "access_token" : token}), 200
    return jsonify({"message": "Bad username or password"}), 401


@account.route('/logout', methods=['POST'])
@jwt_required(fresh=True)
def logout():
    # To logout, discard the client-side token (to be implemented in the client-side app)
    return jsonify({"message": "Logged out."}), 200


@account.route('/register', methods=['POST'])
def register():
    # Parse JSON data sent with the request
    data = request.get_json()
    # Check if the username is already in use
    success = model.register_account(data)
    if success == 1:
        return jsonify({"message": "The registration was succesful"}), 200
    elif success == 0:
        return jsonify({"message": "The account already exists"}), 401
    else:
        return jsonify({"message": "Registration error"}), 400


@account.route('/updateinfo', methods=['POST'])
@jwt_required(fresh=True)
def update_info():
    # Parse JSON data sent with the request
    data = request.get_json()
    # Retrieve the JWT token
    token = request.headers.get('Authorization', None)
    # Modify account info if the token is valid
    if model.update_account_info(token, data):    
        return jsonify({"message": "User info updated"}), 200
    else:
        return jsonify({"message": "Token not valid"}), 401


@account.route('/authenticate', methods=['GET'])
@jwt_required()
def authenticate():
    # Retrieve the JWT token
    token = request.headers.get('Authorization', None)
    # Check if the token is valid and return the associated user
    user, role = model.authenticate_token(token)
    if user is not None:
        return jsonify({"message": "User authenticated", "user": user, "role": role}), 200
    else:
        return jsonify({"message": "Token not valid", "user": None, "role": None}), 401
    

@account.route('/changepassword', methods=['GET'])
@jwt_required(fresh=True)
def changepassword():
    return jsonify({"msg": "Access granted"})


@account.route('/addaccount', methods=['GET'])
@jwt_required(fresh=True)
def addaccount():
    return jsonify({"msg": "Access granted"})


@account.route('/suspendaccount', methods=['GET'])
@jwt_required(fresh=True)
def suspendaccount():
    return jsonify({"msg": "Access granted"})