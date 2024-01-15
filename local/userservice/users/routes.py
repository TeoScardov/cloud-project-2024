from flask import request, jsonify
from .__init__ import users_blueprint, users_db
from .model import save_users
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@users_blueprint.route('/')
def index():
    return "test"

@users_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Verify username and password
    if username in users_db and users_db[username]['password'] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401

@users_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # To logout, discard the client-side token
    return jsonify({"message": "Logged out. Please discard your token."}), 200

@users_blueprint.route('/register', methods=['POST'])
def register():
    # Extract user data from request
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    # Add user to the in-memory users_db
    if username not in users_db:
        users_db[username] = {'password': password, 'role': 'user', 'info': ''}
        save_users(users_db)  # Save the updated users_db back to the file
        return jsonify({"message": "User registered"}), 200
    else:
        return jsonify({"message": "Username already exists"}), 400

# Example protected route
@users_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"msg": "Access granted"})

@users_blueprint.route('/updateinfo', methods=['POST'])
@jwt_required()
def update_info():
    current_user = get_jwt_identity()
    new_info = request.json.get('info', {})

    if current_user in users_db:
        users_db[current_user]['info'] = new_info
        save_users(users_db)  # Update the file with new info
        return jsonify({"message": "User info updated"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Add more routes for changePassword, addAccount, suspendAccount
