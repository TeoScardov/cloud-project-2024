import requests
from flask import jsonify, make_response
from purchaseApp.models import PaymentDao, PurchaseDao, PurchaseItemDao

def isAuthenticated(request):
    """
    This function is used to authenticate a user based on the token provided in the request header.
    It sends a POST request to the authentication service with the token.
    If the authentication is successful, it returns the response from the authentication service and the status code.
    If the authentication fails, it returns a JSON response with an error message and a status code of 500.

    :param 
    request: The request object containing the token in the header.

    Returns:
    The response from the authentication service.
    or 
    A JSON response with an error message and a status code of 500.
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
    """
    This function is used to create a new purchase in the database.
    It sends a POST request to the purchase service with the purchase data.
    If the purchase is created successfully, it returns the response from the purchase service.
    If the purchase creation fails, it returns a JSON response with an error message and a status code of 500.

    :param
    purchase_data: dict The purchase data to be saved in the database.
    account_id: str The unique identifier of the account making the purchase.

    Returns:
    The response from the purchase service.
    or
    A JSON response with an error message and a status code of 500.
    """
    try:

        total_price = purchase_data['cart']['total_price']

        purchase = PurchaseDao(account_id=account_id, total_price=total_price, status="PENDING")

        purchase.save()

        return jsonify({
            'status': 'success',
            'message': 'Purchase created',
            'purchase': purchase
        }), 200
    
    except Exception as e:
        print(e)

        purchase.rollback()

        return jsonify({
            'status': 'error',
            'message': 'Purchase failed',
            'error': e
        }), 500


def performPayment(purchase, auth_token):
    """
    This function is used to perform a payment for a purchase.
    It sends a POST request to the payment service with the purchase id.
    If the payment is successful, it returns the response from the payment service.
    If the payment fails, it returns a JSON response with an error message and a status code of 500.

    :param
    purchase: PurchaseDao The purchase object for which the payment is to be made.
    auth_token: str The authentication token for the user making the purchase.

    Returns:
    The response from the payment service.
    or
    A JSON response with an error message and a status code of 500.
    """

    SERVICE = "http://payment_service:4000/api/payment/"

    #data_payment = purchase[]
    data_payment = {"amount": 30, "card" : 3344567826351444, "cvv" : 366, "expiration" : "12/27", "billing_address": "Via Ciao Ciao 36"}

    try:

        #call payment
        payment_responce = requests.post(SERVICE, json=data_payment, headers={'Authorization': auth_token})

        if payment_responce.status_code != 200:
            return jsonify({
                'status': 'error',
                'message': 'Payment failed'
            }), 500
        
        payment = PaymentDao(purchase_id=purchase.id)
        purchase.status = "APPROVED"
        purchase.save()

        payment.save()

        return jsonify({
            'status': 'success',
            'message': 'Payment successful',
            'payment': payment
        }), 200
    
    except Exception as e:

        payment.rollback()
        purchase.status = "REJECTED"
        purchase.save()

        print(e)
        return jsonify({
            'status': 'error',
            'message': 'Payment failed',
            'error': e
        }), 500


def associateBooksToPurchase(purchase, purchase_data):
    """
    This function is used to associate books to a purchase in the database.
    It sends a POST request to the purchase service with the purchase id and the list of books.
    If the books are associated successfully, it returns a JSON response with a success message and a status code of 200.
    If the association fails, it returns a JSON response with an error message and a status code of 500.

    :param
    purchase: PurchaseDao The purchase object to which the books are to be associated.
    purchase_data: dict The purchase data containing the list of books to be associated.

    Returns:
    A JSON response with a success message and a status code of 200.
    or
    A JSON response with an error message and a status code of 500.
    """

    try:
        purchase_id = purchase.id

        list_of_books = []

        for book in purchase_data['cart']['books']:
            
            purchase_item = PurchaseItemDao(order_id=purchase_id, product_id=book['id'])
            list_of_books.append(purchase_item)

        for item in list_of_books:
            item.save()

        return jsonify({
            'status': 'success',
            'message': 'Books associated to purchase'
        }), 200

    except Exception as e:

        for item in list_of_books:
            item.rollback()

        print(e)
        return jsonify({
            'status': 'error',
            'message': 'Associate books to purchase failed',
            'error': e
        }), 500
    

def associateBooksToAccount(account_id, purchase_data, auth_token):
    """
    This function is used to associate books to an account in the database.
    It sends a POST request to the account service with the account id and the list of books.
    If the books are associated successfully, it returns the response from the account service.
    If the association fails, it returns a JSON response with an error message and a status code of 500.

    :param
    account_id: str The unique identifier of the account to which the books are to be associated.
    purchase_data: dict The purchase data containing the list of books to be associated.

    Returns:
    The response from the account service.
    or
    A JSON response with an error message and a status code of 500.
    """

    SERVICE = "http://account_management:4000/api/account/update"

    books = []
    try:

        for book in purchase_data['cart']['books']:
            
            books.append(book['id'])

        data = {
            'account_id': account_id,
            'library': {
                'add': books,
                'delete': []
            }
        }

        response = requests.post(SERVICE, json=data, headers={'Authorization': auth_token})

        if response.status_code != 200:
            return None

        return response
    
    except Exception as e:
        
        print(e)
        return jsonify({
            'status': 'error',
            'message': 'Associate books to account failed',
            'error': e
        }), 500
    

def clearCart(cart_id, auth_tocken):
    """
    This function is used to clear the cart after a successful purchase.
    It sends a POST request to the cart service with the cart_id.
    If the cart is cleared successfully, it returns the response from the cart service.
    If the cart clearing fails, it returns a JSON response with an error message and a status code of 500.

    :param
    cart_id: str The unique identifier of the cart to be cleared.

    Returns:
    The response from the cart service.
    or
    A JSON response with an error message and a status code of 500.
    """

    SERVICE = 'http://localhost:5000/api/cart/removeCart'

    try:

        response = requests.delete(SERVICE, json={"cart_id": cart_id}, headers={'Authorization': auth_tocken})
        
        return response 
    
    except Exception as e:

        response = make_response(jsonify({
            'status': 'error',
            'message': 'Clear cart failed',
            'error': e
            }), 500)
        
        return response
    