from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import jwt_required
from purchaseApp.controller import *

blueprint = Blueprint('purchase', __name__)

@blueprint.route("/", methods=['GET'])
def health():
    return jsonify(
        status="UP"
    )


@blueprint.route('/', methods=['POST'])
@jwt_required()
def placeOrder():

    #check if user is authenticated and get user info
    auth_responce = isAuthenticated(request)

    if auth_responce.status_code != 200:
        return auth_responce

    #return responce

    account_id = auth_responce.data['account_id']

    purchase_data = request.get_json()

    #try to create a new purchase
    try:
        #create purchase
        purchase = createNewPurchase(request)

        #call payment
        payment = performPayment(purchase)

        associateBooksToPurchase(purchase, request)

        #add books to account
        associateBooksToAccount(purchase, request)

        #clear the cart
        #clearCart(cart_id)

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


