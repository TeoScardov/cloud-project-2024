from flask import Blueprint
from flask import request
from flask import jsonify
import requests

from .Purchase.PurchaseController import PurchaseController

purchase_bp = Blueprint('purchase', __name__)


@purchase_bp.route('/purchase/place', methods=['POST'])
def placeOrder():
    purchase = PurchaseController()
    user_token = request.json['user_token']
    products = request.json['products']

    purchase.placePurchase(user_token, products)

    return jsonify(), 200

@purchase_bp.route('/purchase/<int:userid>', methods=['GET'])
def getUserToken(userid):
    purchase = PurchaseController()
    url = 'http://127.0.0.1:5000/api/user/'+str(userid)+'/token'
    token = requests.post(url).json()['token']

    return jsonify(purchase.getUserToken(token)), 200


@purchase_bp.route('/purchase/commit', methods=['POST'])
def commitPurchase():
    purchase = PurchaseController()
    purchase_id = request.json['purchase_id']

    return jsonify(purchase.commitPurchase(purchase_id)), 200


@purchase_bp.route('/purchase/add', methods=['POST'])
def addPurchasedProduct():
    purchase = PurchaseController()
    purchases = request.json['purchases']

    return jsonify(purchase.addPurchasedProduct(purchases)), 200
