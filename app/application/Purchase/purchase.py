from flask import Blueprint
from flask import request
from flask import jsonify
from .models import Purchase
import requests

purchase_bp = Blueprint('purchase', __name__)

@purchase_bp.route("/health")
def health():
    return jsonify(
        status="UP"
    )

@purchase_bp.route('/place', methods=['POST'])
def placeOrder():
    #Check if user is authenticated
    user_token = request.authorization.__str__()[7:-1]

    if user_token == 'None':
        return jsonify({
            'status': 'error',
            'message': 'User not authenticated'
        }), 401
    else:

        return jsonify({
                'status': 'success',
                'userToken': user_token
            }), 200


@purchase_bp.route('/<int:userid>', methods=['GET'])
def getUserToken(userid):
    url = 'http://127.0.0.1:5000/api/user/'+str(userid)+'/token'
    token = requests.post(url).json()['token']

    return jsonify({
            'status': 'success',
            'getUserToken': token
        }), 200


@purchase_bp.route('/commit', methods=['POST'])
def commitPurchase():
    purchase_id = request.json['purchase_id']

    return jsonify({
            'status': 'success',
            'commitPurchase': purchase_id
        }), 200


@purchase_bp.route('/add', methods=['POST'])
def addPurchasedProduct():
    purchases = request.json['purchases']

    return jsonify({
            'status': 'success',
            'addPurchasedProduct': purchases
        }), 200
