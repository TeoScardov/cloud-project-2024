import re
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

    return "Purchase service is up and running &#128640;", 200

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

    try:
        
        # check if user is authenticated and get user info
        auth_responce = isAuthenticated(request)

        if auth_responce.status_code != 200:
            return auth_responce

        # get account_id from auth_responce
        account_id = auth_responce.get_json().get('account_id')
        # get auth token 
        auth = request.headers['Authorization']
        # get purchase data from request
        purchase_data = request.get_json()
    
    except Exception as e:
        return make_response(jsonify({
                'status': 'error',
                'message': 'Failed to get data from request, check for missing fields',
                'error': e
            }), 500)

    # create new purchase
    return createNewPurchase(purchase_data, account_id)

    
@blueprint.route('/payment', methods=['POST'])
@jwt_required()
def payPurchase():
    """
    This function is used to pay for a purchase.
    It first checks if the user is authenticated.
    It gets the auth token.
    It gets the purchase by its id.
    It performs payment.
    If the payment is successful, it returns a JSON response with a success message and a status code of 200.
    If the payment fails, it returns a JSON response with an error message and a status code of 500.
    """

    try:
        # check if user is authenticated
        auth_responce = isAuthenticated(request)

        if auth_responce.status_code != 200:
            return auth_responce
        
        # get user id
        account_id = auth_responce.get_json().get('account_id')

        # get auth token
        auth_token = request.headers['Authorization']

        # get purchase data from request
        purchase_data = request.get_json()
    
    except Exception as e:
        return make_response(jsonify({
                'status': 'error',
                'message': 'Failed to get data from request, check for missing fields',
                'error': e
            }), 500)

    # perform payment
    return performPayment(purchase_data, auth_token, account_id)
    

@blueprint.route('/add-book-to-purchase', methods=['POST'])
@jwt_required()
def addBookToPurchase():
    """
    This function is used to add a book to a purchase.
    It first checks if the user is authenticated.
    It gets the auth token.
    It gets the purchase by its id.
    It gets the book by its id.
    It adds the book to the purchase.
    If the book is added to the purchase successfully, it returns a JSON response with a success message and a status code of 200.
    If the book is not added to the purchase successfully, it returns a JSON response with an error message and a status code of 500.
    """

    try:
        # check if user is authenticated
        auth_responce = isAuthenticated(request)

        if auth_responce.status_code != 200:
            return auth_responce
        
        # get user id
        account_id = auth_responce.get_json().get('account_id')
        
        # get auth token
        auth_token = request.headers['Authorization']
        
        # get purchase data from request
        purchase_data = request.get_json()
    
    except Exception as e:
        return make_response(jsonify({
                'status': 'error',
                'message': 'Failed to get data from request, check for missing fields',
                'error': e
            }), 500)
    
    # add book to purchase
    return associateBooksToPurchase(purchase_data, account_id)
    

@blueprint.route('/add-book-to-account', methods=['POST'])
@jwt_required()
def addBookToAccount():
    """
    This function is used to add a book to an account.
    It first checks if the user is authenticated.
    It gets the auth token.
    It gets the book by its id.
    It adds the book to the account.
    If the book is added to the account successfully, it returns a JSON response with a success message and a status code of 200.
    If the book is not added to the account successfully, it returns a JSON response with an error message and a status code of 500.
    """

    try:
        # check if user is authenticated
        auth_responce = isAuthenticated(request)

        if auth_responce.status_code != 200:
            return auth_responce
        
        # get user id
        account_id = auth_responce.get_json().get('account_id')
        
        # get auth token
        auth_token = request.headers['Authorization']
        
        # get purchase data from request
        purchase_data = request.get_json()
    
    except Exception as e:
        return make_response(jsonify({
                'status': 'error',
                'message': 'Failed to get data from request, check for missing fields',
                'error': e
            }), 500)
    
    # add book to account
    return associateBooksToAccount(account_id, purchase_data, auth_token)

    
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

    try:
        # check if user is authenticated
        auth_responce = isAuthenticated(request)

        if auth_responce.status_code != 200: # type: ignore
            return auth_responce
        
        # get user id
        account_id = auth_responce.get_json().get('account_id')
    
    except Exception as e:
        return make_response(jsonify({
                'status': 'error',
                'message': 'Failed to get data from request, check for missing fields',
                'error': e
            }), 500)

    return getPurchaseByAccountId(account_id)


