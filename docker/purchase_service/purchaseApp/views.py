from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import jwt_required
from purchaseApp.controller import performPayment, createNewPurchase, associateBooksToPurchase, associateBooksToAccount, isAuthenticated

import requests

blueprint = Blueprint('purchase', __name__)

@blueprint.route("/", methods=['GET'])
def health():
    return jsonify(
        status="UP"
    )


@blueprint.route('/', methods=['POST'])
@jwt_required()
def placeOrder():
    #check login
    responce = isAuthenticated(request)

    if responce['status_code'] == 500:
        return jsonify({
                'status': 'error',
                'message': 'Authentication failed'
            }), 500
    elif responce['status_code'] == 401:
        return jsonify({
                'status': 'error',
                'message': 'Unauthorized'
            }), 401
    else:
        pass

    try:
        #create purchase
        purchase = createNewPurchase(request)

        #call payment
        payment = performPayment(purchase)

        associateBooksToPurchase(purchase, request)

        #add books to account
        associateBooksToAccount(purchase, request)

        #get the username
        #username = get_username(request)

        #get the cart
        #cart = get_cart(username)

        #create the purchase
        #purchase = Purchase(username, cart)

        #clear the cart
        #clearCart(username)

        return jsonify({
                'status': 'success',
            }), 200
    except:
        return jsonify({
                'status': 'error',
                'message': 'Purchase failed'
            }), 500

@blueprint.route('/details', methods=['GET'])
#@jwt_required()
def getPurchaseDetails():
    purchase_id = request.get_json()

    #purchase = Purchase.get_purchase(purchase_id)

    return jsonify({
            'status': 'success',
            'purchase': purchase_id#purchase.to_dict()
        }), 200


