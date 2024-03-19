from flask import Blueprint
from flask import request
from flask import jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/authenticate', methods=['POST'])
def authenticate():
    
    if request.authorization is None:
        return jsonify({
            'status': 'error',
            'authenticate': 'Not authenticated'
        }), 401
    else:
        return jsonify({
            "message": "User authenticated",
            "role": "admin",
            "username": "user1"
        }), 200
