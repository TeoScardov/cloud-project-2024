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
    ---
    responses:
        200:
            description: Purchase service is up and running
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
    It gets the auth token from the headers.
    It gets the purchase data from the request.
    It creates a new purchase.
    If the purchase is created successfully, it returns a JSON response with the purchase data and a status code of 200.
    If the purchase is not created successfully, it returns a JSON response with an error message and a status code of 500.
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer token
        - name: purchase_data
          in: body
          required: true
          schema:
            type: object
            properties:
                cart:
                    type: object
                    properties:
                        total: 
                            type: integer
                            description: Total amount of the purchase
    
    responses:
        200:
            description: Purchase process successful
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Purchase process successful
                    status:
                        type: string
                        description: success
                    purchase:
                        type: object
                        properties:
                            id:
                                type: string
                                description: Purchase id
                            account_id:
                                type: string
                                description: Account id
                            order_date:
                                type: string
                                description: Order date
                            status:
                                type: string
                                description: Purchase status
                            total:
                                type: integer
                                description: Total amount of the purchase
        
        500:
            description: Failed to get data from request | Purchase creation failed
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Purchase creation failed
                    status:
                        type: string
                        description: error
                    error:
                        type: string
                        description: Error message

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
    If the user is authenticated, it gets the user info.
    It then gets the account_id from the auth_responce.
    It gets the auth token from the headers.
    It gets the payment data from the request.
    It performs payment.
    If the payment is successful, it returns a JSON response with a success message and a status code of 200.
    If the payment fails, it returns a JSON response with an error message and a status code of 500.
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer token
        - name: payment_data
          in: body
          required: true
          schema:
            type: object
            properties:
                billing_address:
                    type: string
                    description: Billing address
                cc: 
                    type: string
                    description: Credit card number
                expiredate:
                    type: string
                    description: Expiry date of the credit card
                cvv:
                    type: string
                    description: CVV number
                purchase:
                    type: object
                    properties:
                        id:
                            type: string
                            description: Purchase id
                        account_id:
                            type: string
                            description: Account id
                        order_date:
                            type: string
                            description: Order date
                        status:
                            type: string
                            description: Purchase status
                        total:
                            type: integer
                            description: Total amount of the purchase
    
    responses:
        200:
            description: Payment successful
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Payment process successful
                    status:
                        type: string
                        description: success
                    payment:
                        type: object
                        properties:
                            id:
                                type: string
                                description: Purchase id
                            purchase_id:
                                type: string
                                description: Purchase id
            
        400:
            description: Purchase already processed
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Purchase already processed
                    status:
                        type: string
                        description: error
        401:
            description: Unauthorized  
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Unauthorized
                    status:
                        type: string
                        description: error      
        404:
            description: Purchase not found | Payment not found
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Purchase not found | Payment not found
                    status:
                        type: string
                        description: error
        500:
            description: Payment rejected | Missing data | Failed to get purchase items | Payment creation failed | Payment retrival failed
            schema:
                type: object
                optional:
                - error
                properties:
                    message:
                        type: string
                        description: Payment rejected | Missing data | Failed to get purchase items | Payment creation failed | Payment retrival failed
                    status:
                        type: string
                        description: error
                    error:
                        type: string
                        description: Error message
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

        # get payment data from request
        payment_data = request.get_json()
    
    except Exception as e:
        return make_response(jsonify({
                'status': 'error',
                'message': 'Failed to get data from request, check for missing fields',
                'error': e
            }), 500)

    # perform payment
    return performPayment(payment_data, auth_token, account_id)
    

@blueprint.route('/add-book-to-purchase', methods=['POST'])
@jwt_required()
def addBookToPurchase():
    """
    This function is used to add a book to a purchase.
    It first checks if the user is authenticated.
    If the user is authenticated, it gets the user info.
    It then gets the account_id from the auth_responce.
    It gets the auth token from the headers.
    It gets the books data from the request.
    It adds the books to the purchase.
    If the books are added to the purchase successfully, it returns a JSON response with a success message and a status code of 200.
    If the books are not added to the purchase successfully, it returns a JSON response with an error message and a status code of 500.
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer token
        - name: book_data
          in: body
          required: true
          schema:
            type: object
            properties:
                cart:
                    type: object
                    properties:
                        items:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        description: Book id

                purchase:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: Purchase id
                        account_id:
                            type: integer
                            description: Account id
    
    responses:
        200:
            description: Book added to purchase successfully
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Book added to purchase successfully
                    status:
                        type: string
                        description: success
        400:
            description: No book to be associated with purchase | Purchase not APPROVED | Purchase already associated with books
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: No book to be associated with purchase | Purchase not APPROVED | Purchase already associated with books
                    status:
                        type: string
                        description: error
        401:
            description: Unauthorized
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Unauthorized
                    status:
                        type: string
                        description: error
        404:
            description: Purchase not found
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Purchase not found
                    status:
                        type: string
                        description: error
            
        500:
            description: Associate books to purchase failed | Missing data | Failed to get purchase items
            schema:
                type: object
                optional:
                - error
                properties:
                    message:
                        type: string
                        description: Associate books to purchase failed | Missing data | Failed to get purchase items
                    status:
                        type: string
                        description: error
                    error:
                        type: string
                        description: Error message
    
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
        book_data = request.get_json()
    
    except Exception as e:
        return make_response(jsonify({
                'status': 'error',
                'message': 'Failed to get data from request, check for missing fields',
                'error': e
            }), 500)
    
    # add book to purchase
    return associateBooksToPurchase(book_data, account_id)
    

@blueprint.route('/add-book-to-account', methods=['POST'])
@jwt_required()
def addBookToAccount():
    """
    This function is used to add a book to an account.
    It first checks if the user is authenticated.
    If the user is authenticated, it gets the user info.
    It then gets the account_id from the auth_responce.
    It gets the auth token from the headers.
    It gets the books data from the request.
    It adds the book to the account.
    If the books are added to the account successfully, it returns a JSON response with a success message and a status code of 200.
    If the books are not added to the account successfully, it returns a JSON response with an error message and a status code of 500.
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer token
        - name: book_data
          in: body
          required: true
          schema:
            type: object
            properties:
                cart:
                    type: object
                    properties:
                        items:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        description: Book id
                purchase:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: Purchase id
                        account_id:
                            type: integer
                            description: Account id
    
    responses:
        200:
            description: Book added to account successfully
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Book added to account successfully
        400:
            description: Purchase items mismatch in number of books | Purchase items mismatch in books
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Purchase items mismatch in number of books | Purchase items mismatch in books
                    status:
                        type: string
                        description: error
        401:
            description: Unauthorized
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Unauthorized
                    status:
                        type: string
                        description: error
        404:
            description: Purchase not found
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Purchase not found
                    status:
                        type: string
                        description: error
        500:
            description: Associate books to account failed | Missing data | Failed to get purchase items | Account service not found
            schema:
                type: object
                optional:
                - error
                properties:
                    message:
                        type: string
                        description: Associate books to account failed | Missing data | Failed to get purchase items | Account service not found
                    status:
                        type: string
                        description: error
                    error:
                        type: string
                        description: Error message
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
    This function is used to get all purchases using the authorization token.
    It first checks if the user is authenticated.
    If the user is authenticated, it gets the user info.
    It then gets the account_id from the auth_responce.
    It gets the auth token from the headers.
    If purchases are found, it returns a JSON response with the purchase data and a status code of 200.
    If no purchases are found, it returns a JSON response with an empty list and a status code of 200.
    If there is some error, it returns a JSON response with an error message and a status code of 500.
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer token

    responses:
        200:
            description: Purchase data | Empty list
            schema:
                type: object
                properties:
                    purchase:
                        type: array
                        items:
                            type: object
                            properties:
                                id:
                                    type: string
                                    description: Purchase id
                                account_id:
                                    type: string
                                    description: Account id
                                order_date:
                                    type: string
                                    description: Order date
                                status:
                                    type: string
                                    description: Purchase status
                                total:
                                    type: integer
                                    description: Total amount of the purchase
        500:
            description: Failed to get purchase data
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Failed to get purchase data
                    status:
                        type: string
                        description: error
                    error:
                        type: string
                        description: Error message
    """

    try:
        # check if user is authenticated
        auth_responce = isAuthenticated(request)

        if auth_responce.status_code != 200:
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


