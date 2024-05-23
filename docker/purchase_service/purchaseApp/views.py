from flask import Blueprint
from flask import request
from flask import jsonify, render_template
from flask_jwt_extended import jwt_required
from purchaseApp.controller import *

blueprint = Blueprint('purchase', __name__)

@blueprint.route("/", methods=['GET'])
def health():
    """
    This function is used to check the health of the purchase service.
    It returns a message indicating that the service is up and running.
    """

    return "Purchase service is up and running &#128640;"



@blueprint.route('/', methods=['POST'])
@jwt_required()
def placeOrder():
    """
    This function is used to place an order.
    It first checks if the user is authenticated.
    If the user is authenticated, it gets the user info.
    It then gets the account_id from the auth_responce.
    It gets the auth token.
    It gets the purchase data from the request.
    It creates a new purchase.
    It performs payment.
    It associates books to purchase.
    It associates books to account.
    It clears the cart.
    If the purchase process is successful, it returns a JSON response with a success message and a status code of 200.
    If the purchase process fails, it returns a JSON response with an error message and a status code of 500.
    """

    # check if user is authenticated and get user info
    auth_responce = isAuthenticated(request)

    if auth_responce.status_code != 200: # type: ignore
        return auth_responce

    # get account_id from auth_responce
    account_id = auth_responce.json()['account_id'] #type: ignore
    # get auth token 
    auth = request.headers['Authorization']
    # get purchase data from request
    purchase_data = request.get_json()

    try:

        # create new purchase
        [purchase_responce, purchase]  = createNewPurchase(purchase_data, account_id)
        if purchase_responce.status_code != 200:
            return purchase_responce

        # perform payment
        [payment_responce, payment] = performPayment(purchase, purchase_data, auth)
        if payment_responce.status_code != 200:
            return payment_responce

        # associate books to purchase
        associate_books_to_purchase = associateBooksToPurchase(purchase, purchase_data)
        if associate_books_to_purchase.status_code != 200: #type: ignore
            return associate_books_to_purchase

        # associate books to account
        associate_books_to_account = associateBooksToAccount(account_id, purchase_data, auth)
        if associate_books_to_account.status_code != 200: #type: ignore
            return associate_books_to_account
        
        # clear the cart
        #cart = clearCart(purchase_data['cart']['cart_id'], auth)
        #if cart.status_code != 200:
        #    return cart
    

        return make_response(jsonify({
                'status': 'success',
            }), 200)
    
    except Exception as e:

        return make_response(jsonify({
                'status': 'error',
                'message': 'Purchase process failed',
                'error': e
            }), 500)
    
@blueprint.route('/orders', methods=['GET'])
@jwt_required()
def getPurchase():
    """
    This function is used to get a purchase by its id.
    It first checks if the user is authenticated.
    It gets the auth token.
    It gets the purchase by its id.
    If the purchase is found, it returns a JSON response with the purchase data and a status code of 200.
    If the purchase is not found, it returns a JSON response with an error message and a status code of 404.
    """

    # check if user is authenticated
    auth_responce = isAuthenticated(request)

    if auth_responce.status_code != 200: # type: ignore
        return auth_responce
    
    # get user id
    account_id = auth_responce.json().get('account_id') # type: ignore

    purchases = getPurchaseByAccountId(account_id)

    return make_response(jsonify({
        'purchase': [purchase.to_dict() for purchase in purchases]
    }), 200)

    


