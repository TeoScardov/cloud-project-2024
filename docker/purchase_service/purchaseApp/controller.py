import requests
import os
from flask import jsonify, make_response, Response
from purchaseApp.models import PaymentDao, PurchaseDao, PurchaseItemDao

SERVICES = {
    "ACCOUNT_SERVICE": os.getenv('ACCOUNT_SERVICE_URL'),
    "PAYMENT_SERVICE": os.getenv('PAYMENT_SERVICE_URL'),
    #"CART_SERVICE": os.getenv('CART_SERVICE_URL')
}

def isAuthenticated(request)-> Response:
    """
    This function is used to authenticate a user.
    It sends a POST request to the account service with the user's auth token.
    If the user is authenticated successfully, it returns the response from the account service.
    If the authentication fails, it returns a JSON response with an error message and a status code of 500.
    
    :param
    request: The request object containing the user's auth token.
    
    Returns:
    The response from the account service.
    or
    A JSON response with an error message and a status code of 500.
    """

    if SERVICES['ACCOUNT_SERVICE'] is None:
        return make_response(jsonify({
            'status': 'error',
            'message': 'Account service not found',
            'error': 'ACCOUNT_SERVICE_URL not set'
        }), 500)

    SERVICE = SERVICES['ACCOUNT_SERVICE'] + "/authenticate"

    try:
        #get token from request
        token = request.headers['Authorization']

        #call authentication service
        response = requests.post(SERVICE, headers={'Authorization': token})

        #return toFlaskResponse(response)
        return make_response(jsonify(response.json()), response.status_code)
    
    except Exception as e:

        return make_response(jsonify({
            'status': 'error',
            'message': 'Authentication failed',
            'error': e
            }), 500)

def createNewPurchase(purchase_data, account_id)-> Response:
    """
    This function is used to create a new purchase.
    It sends a POST request to the purchase service with the purchase data.
    If the purchase is created successfully, it returns a JSON response with a success message and a status code of 200.
    If the creation fails, it returns a JSON response with an error message and a status code of 500.
    
    :param
    purchase_data: dict The purchase data containing the total price and the status of the purchase.
    account_id: str The unique identifier of the account making the purchase.
    
    Returns:
    A JSON response with a success message and a status code of 200.
    or
    A JSON response with an error message and a status code of 500.
    """
    
    try:

        total = purchase_data['cart']['total']

        purchase = PurchaseDao(account_id=account_id, total=total, status="PENDING")

        purchase.save()

        return make_response(jsonify({
            'status': 'success',
            'message': 'Purchase created',
            'purchase': purchase.to_dict()
        }), 200)
    
    except Exception as e:
        print(e)

        purchase.rollback()

        return make_response(jsonify({
            'status': 'error',
            'message': 'Purchase creation failed',
            'error': e
        }), 500)


def performPayment(purchase_data, auth_token, account_id)-> Response:
    """
    This function is used to perform payment for a purchase.
    It sends a POST request to the payment service with the purchase data.
    If the payment is successful, it returns a JSON response with a success message and a status code of 200.
    If the payment fails, it returns a JSON response with an error message and a status code of 500.
    
    :param
    purchase_data: dict The purchase data containing the payment details.
    auth_token: str The authentication token of the user.
    account_id: str The unique identifier of the account making the purchase.
    
    Returns:
    A JSON response with a success message and a status code of 200.
    or
    A JSON response with an error message and a status code of 500.
    """
    
    if SERVICES['PAYMENT_SERVICE'] is None:
        return make_response(jsonify({
            'status': 'error',
            'message': 'Payment service not found',
            'error': 'PAYMENT_SERVICE_URL not set'
        }), 500)

    SERVICE = SERVICES['PAYMENT_SERVICE']

    try:

        purchase = PurchaseDao.get_by_id(purchase_data['purchase']['id'])

        if purchase is None:
            return make_response(jsonify({
                'status': 'error',
                'message': 'Purchase not found',
            }), 404)
            
        if str(purchase.account_id) != str(account_id):
            return make_response(jsonify({
                'status': 'error',
                'message': 'Unauthorized',
            }), 401)

        data_payment = {
            'total': purchase_data['purchase']['total'],
            'billing_address': purchase_data['billing_address'],
            'cc': purchase_data['cc'],
            'expiredate': purchase_data['expiredate'],
            'cvv': purchase_data['cvv'],
        }
    
    except Exception as e:
        print(e)
        return make_response(jsonify({
            'status': 'error',
            'message': 'Missing data',
            'error': e
        }), 500)
        
        
    try:
        
        if purchase.status == "APPROVED":
            return make_response(jsonify({
                'status': 'error',
                'message': 'Purchase already processed',
            }), 400)
            
        if purchase.status == "REJECTED":
            payment = PaymentDao.get_by_purchase_id(purchase.id)
            
            if payment is None:
                return make_response(jsonify({
                    'status': 'error',
                    'message': 'Payment not found',
                }), 404)

        else:
            payment = PaymentDao(purchase_id=purchase.id)
            
            if payment is None:
                return make_response(jsonify({
                    'status': 'error',
                    'message': 'Payment creation failed',
                }), 500)
    
    except Exception as e:
        print(e)
        return make_response(jsonify({
            'status': 'error',
            'message': 'Payment retrival failed',
            'error': e
        }), 500)
      
  
    try:
        #call payment
        payment_responce = requests.post(SERVICE, json=data_payment, headers={'Authorization': auth_token})

        if payment_responce.status_code != 200:
            
            purchase.status = "REJECTED"
            purchase.save()
            
            return make_response(jsonify({
                'status': 'error',
                'message': 'Payment rejected',
                'error': payment_responce.json()
            }), 500)
    
    except Exception as e:
        
        purchase.status = "REJECTED"
        purchase.save()
        
        return make_response(jsonify({
            'status': 'error',
            'message': 'Payment rejected',
            'error': e
        }), 500)
    
    
    
    try:
        
        purchase.status = "APPROVED"                  
        purchase.save()
            
        payment.save()

        return make_response(jsonify({
            'status': 'success',
            'message': 'Payment successful',
            'payment': payment.to_dict()
        }), 200)
    
    except Exception as e:

        payment.rollback()
        purchase.status = "REJECTED"
        purchase.save()

        return make_response(jsonify({
            'status': 'error',
            'message': 'Payment rejected',
            'error': e
        }), 500)


def associateBooksToPurchase(purchase_data, account_id) -> Response:
    """
    This function is used to associate books to a purchase.
    It sends a POST request to the purchase service with the purchase id and the list of books.
    If the books are associated successfully, it returns the response from the purchase service.
    If the association fails, it returns a JSON response with an error message and a status code of 500.
    
    :param
    purchase_data: dict The purchase data containing the list of books to be associated.
    account_id: str The unique identifier of the account to which the books are to be associated.
    
    Returns:
    The response from the purchase service.
    or
    A JSON response with an error message and a status code of 500.
    """

    try:
        purchase = PurchaseDao.get_by_id(purchase_data['purchase']['id'])

        if purchase is None:
            return make_response(jsonify({
                'status': 'error',
                'message': 'Purchase not found',
            }), 404)
            
        if str(purchase.account_id) != str(account_id):
            return make_response(jsonify({
                'status': 'error',
                'message': 'Unauthorized',
            }), 401)

        books = purchase_data['cart']['items']
        isbns = [book['isbn'] for book in books]
        
        if len(isbns) == 0:
            return make_response(jsonify({
                'status': 'error',
                'message': 'No books to associate',
            }), 400)

    except Exception as e:
        return make_response(jsonify({
            'status': 'error',
            'message': 'Missing data',
            'error': e
        }), 500)


        
    try:
        purchase_items = PurchaseItemDao.get_by_order_id(purchase.id)

        if purchase_items is not None:
            return make_response(jsonify({
                'status': 'error',
                'message': 'Purchase already associated with books',
            }), 400)
    
    except Exception as e:
        return make_response(jsonify({
            'status': 'error',
            'message': 'Failed to get purchase items',
            'error': e
        }), 500)
    
    
    try:
        purchase_items = PurchaseItemDao(order_id=purchase.id, product_id=isbns)

        purchase_items.save()

        return make_response(jsonify({
            'status': 'success',
            'message': 'Books associated to purchase'
        }), 200)

    except Exception as e:

        return make_response(jsonify({
            'status': 'error',
            'message': 'Associate books to purchase failed',
            'error': e
        }), 500)
    

def associateBooksToAccount(account_id, purchase_data, auth_token) -> Response:
    """
    This function is used to associate books to an account.
    It sends a POST request to the account service with the account id and the list of books.
    If the books are associated successfully, it returns the response from the account service.
    If the association fails, it returns a JSON response with an error message and a status code of 500.
    
    :param
    account_id: str The unique identifier of the account to which the books are to be associated.
    purchase_data: dict The purchase data containing the list of books to be associated.
    auth_token: str The authentication token of the user.
    
    Returns:
    The response from the account service.
    or
    A JSON response with an error message and a status code of 500.
    """
    
    if SERVICES['ACCOUNT_SERVICE'] is None:
        return make_response(jsonify({
            'status': 'error',
            'message': 'Account service not found',
            'error': 'ACCOUNT_SERVICE_URL not set'
        }), 500)

    SERVICE = SERVICES['ACCOUNT_SERVICE'] + "/update"

    try:
        
        books = purchase_data['cart']['items']
        isbns = [book['isbn'] for book in books]
    
        purchase = PurchaseDao.get_by_id(purchase_data['purchase']['id'])
        if purchase is None:
            return make_response(jsonify({
                'status': 'error',
                'message': 'Purchase not found',
            }), 404)
        
        if str(purchase.account_id) != str(account_id):
            return make_response(jsonify({
                'status': 'error',
                'message': 'Unauthorized',
            }), 401)
        
        purchase_items = PurchaseItemDao.get_by_order_id(purchase.id)
        
        if purchase_items is None:
            return make_response(jsonify({
                'status': 'error',
                'message': 'Purchase items not found',
            }), 404)
            
        if len(purchase_items.product_id) != len(books):
            return make_response(jsonify({
                'status': 'error',
                'message': 'Purchase items mismatch in number of books',
            }), 400)
        
        if set(purchase_items.product_id) != set(isbns):
            return make_response(jsonify({
                'status': 'error',
                'message': 'Purchase items mismatch in books',
            }), 400)
    
    except Exception as e:
        return make_response(jsonify({
            'status': 'error',
            'message': 'Missing data',
            'error': e
        }), 500)


    try:

        data = {
            'account_id': account_id,
            'library': {
                'add': isbns,
                'delete': []
            }
        }

        response = requests.post(SERVICE, json=data, headers={'Authorization': auth_token})

        if response.status_code != 200:
            return make_response(jsonify({
                'status': 'error',
                'message': 'Associate books to account failed',
                'error': response.json()
            }), 500)

        return make_response(jsonify(response.json()), response.status_code)
    
    except Exception as e:
        
        print(e)
        return make_response(jsonify({
            'status': 'error',
            'message': 'Associate books to account failed',
            'error': e
        }), 500)
    

# def clearCart(cart_id, auth_tocken):
#     """
#     This function is used to clear the cart after a successful purchase.
#     It sends a POST request to the cart service with the cart_id.
#     If the cart is cleared successfully, it returns the response from the cart service.
#     If the cart clearing fails, it returns a JSON response with an error message and a status code of 500.

#     :param
#     cart_id: str The unique identifier of the cart to be cleared.

#     Returns:
#     The response from the cart service.
#     or
#     A JSON response with an error message and a status code of 500.
#     """

#     SERVICE = 'http://localhost:5000/api/cart/removeCart'

#     try:

#         response = requests.delete(SERVICE, json={"cart_id": cart_id}, headers={'Authorization': auth_tocken})
        
#         return response 
    
#     except Exception as e:

#         response = make_response(jsonify({
#             'status': 'error',
#             'message': 'Clear cart failed',
#             'error': e
#             }), 500)
        
#         return response
    

def getPurchaseByAccountId(account_id):
    """
    This function is used to get all purchases made by a user.
    It sends a GET request to the purchase service with the user_id.
    If the purchases are retrieved successfully, it returns the response from the purchase service.
    If the retrieval fails, it returns a JSON response with an error message and a status code of 500.

    :param
    user_id: str The unique identifier of the user.

    Returns:
    The response from the purchase service.
    or
    A JSON response with an error message and a status code of 500.
    """
    
    try:
        
        purchases = PurchaseDao.get_by_account_id(account_id=account_id)
        
        return make_response(jsonify({
            'purchase': [purchase.to_dict() for purchase in purchases]
        }), 200)
        
    except Exception as e:
            
        return make_response(jsonify({
            'status': 'error',
            'message': 'Get purchase failed',
            'error': e
        }), 500)

