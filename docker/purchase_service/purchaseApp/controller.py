import requests
import flask
from flask import jsonify, make_response
from purchaseApp.models import PaymentDao, PurchaseDao, PurchaseItemDao
from purchaseApp.utils import toFlaskResponse

def isAuthenticated(request: flask.Request)-> requests.Response:
    """
    This function is used to authenticate a user based on the token provided in the request header.
    It sends a POST request to the authentication service with the token.
    If the authentication is successful, it returns the response from the authentication service and the status code.
    If the authentication fails, it returns a JSON response with an error message and a status code of 500.

    :param 
    request: flask.Request The request object containing the token in the header.

    Returns:
    flask.Response: The response from the authentication service.
    """

    SERVICE = "http://account_management:4000/api/account/authenticate"

    try:
        #get token from request
        token = request.headers['Authorization']

        #call authentication service
        response = requests.post(SERVICE, headers={'Authorization': token})

        #return toFlaskResponse(response)
        return response
    
    except Exception as e:

        response = jsonify({
            'status': 'error',
            'message': 'Authentication failed',
            'error': e
            }), 500
        
        return response # type: ignore

def createNewPurchase(purchase_data, account_id):
    try:

        total_price = purchase_data['cart']['total_price']

        purchase = PurchaseDao(account_id=account_id, total_price=total_price, status="PENDING")

        purchase.save()
        return purchase
    
    except Exception as e:
        print(e)

        return None


def performPayment(purchase, auth_token):

    try:
        #getPriceFromCart = requests.get('http://localhost:5000/api/cart/price/' + purchase_id)

        data_payment = {"amount": 30, "card" : 3344567826351444, "cvv" : 366, "expiration" : "12/27", "billing_address": "Via Ciao Ciao 36"}

        #call payment
        payment = requests.post('http://payment_service:4000/api/payment/', json=data_payment, headers={'Authorization': auth_token})

        if payment.status_code != 200:
            return None
        
        return payment.json()
    
    except Exception as e:
        print(e)
        return None


    try:
        purchase_id = purchase.id

        payment = PaymentDao(purchase_id=purchase_id)
        purchase.status = "APPROVED"

        purchase.save()
        payment.save()
        return payment
    except Exception as e:
        print(e)
        return None
    
def get_payment_by_id(payment_id):
    return PaymentDao.get_by_id(payment_id)

def associateBooksToPurchase(purchase, purchase_data):
    try:
        purchase_id = purchase.id

        for book in purchase_data['books']:
            purchase_item = PurchaseItemDao(order_id=purchase_id, product_id=book['id'])
            purchase_item.save()
        
        return True

    except Exception as e:
        print(e)
        return None
    
def associateBooksToAccount(purchase, purchase_data):
    try:
        account_id = purchase.account_id

        for book in purchase_data['books']:
            #associate book to account
            pass

        return True
    
    except Exception as e:
        print(e)
        return None
    

def clearCart(cart_id: str)-> flask.Response:
    """
    This function is used to clear the cart after a successful purchase.
    It sends a POST request to the cart service with the cart_id.
    If the cart is cleared successfully, it returns the response from the cart service.
    If the cart clearing fails, it returns a JSON response with an error message and a status code of 500.

    :param
    cart_id: str The unique identifier of the cart to be cleared.

    Returns:
    flask.Response: The response from the cart service.
    """

    SERVICE = 'http://localhost:5000/api/cart/removeProduct'

    try:

        response = requests.post(SERVICE, json={"cart_id": cart_id})
        return toFlaskResponse(response)
    
    except Exception as e:

        response = make_response(jsonify({
            'status': 'error',
            'message': 'Clear cart failed',
            'error': e
            }), 500)
        
        return response
    