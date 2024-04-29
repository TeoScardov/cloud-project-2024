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
    account_id = auth_responce.json()['account_id']
    auth = request.headers['Authorization']
    purchase_data = request.get_json()

    #try to create a new purchase
    try:

        #create purchase
        purchase = createNewPurchase(purchase_data, account_id)

        if purchase is None:
            return jsonify({
                'status': 'error',
                'message': 'Purchase failed',
                'price': purchase_data['cart']['total_price']
            }), 500
    
        #call payment
        payment = performPayment(purchase, auth)

        if payment is None:
            return jsonify({
                'status': 'error',
                'message': 'Payment failed'
            }), 500

        if associateBooksToPurchase(purchase, purchase_data) is None:
            return jsonify({
                'status': 'error',
                'message': 'Purchase failed'
            }), 500


        #add books to account
        if associateBooksToAccount(purchase, purchase_data) is None:
            return jsonify({
                'status': 'error',
                'message': 'Purchase failed'
            }), 500

        #clear the cart
        #clearCart(cart_id)
    
        return jsonify({
                'status': 'success',
                'purchase_id': purchase.id,
                'payment_id': payment.id
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


