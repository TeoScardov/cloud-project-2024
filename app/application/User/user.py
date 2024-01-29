from flask import Blueprint
from flask import request
from flask import jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('<id>/token', methods=['POST'])
def token(id):
    return jsonify({'token' : int(id)*33}), 200