import requests
from purchaseApp.models import PaymentDao, PurchaseDao, PurchaseItemDao

def isAuthenticated(request):
    try:
        #get token from request
        token = request.headers['Authorization']

        #call authentication service
        response = requests.post('http://account_management:4000/api/account/authenticate', headers={'Authorization': token})

        return response.json()
    
    except Exception as e:
        print(e)
        return {'status_code': 500, 'message': 'Internal server error'}

def createNewPurchase(request):
    try:
        account_id = request.get_json()['account_id']
        cart = request.get_json()['cart']

        total_price = cart['total_price'] #something like that

        purchase = PurchaseDao(account_id=account_id, total_price=total_price, status="PENDING")

        purchase.save()
        return purchase
    except Exception as e:
        print(e)
        return None


def performPayment(purchase):

    try:
        #getPriceFromCart = requests.get('http://localhost:5000/api/cart/price/' + purchase_id)

        data_payment = {"amount": 30, "card" : 3344567826351444, "cvv" : 366, "expiration" : "12/27", "billing_address": "Via Ciao Ciao 36"}

        #call payment
        payment = requests.post('http://localhost:5001/api/payment/', json=data_payment)

        if payment.status_code != 200:
            return None
    
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

def associateBooksToPurchase(purchase, request):
    try:
        purchase_id = purchase.id
        cart = request.get_json()['cart']

        for book in cart['books']:
            purchase_item = PurchaseItemDao(order_id=purchase_id, product_id=book['id'])
            purchase_item.save()
    except Exception as e:
        print(e)
        return None
    
def associateBooksToAccount(purchase, request):
    try:
        account_id = purchase.account_id
        cart = request.get_json()['cart']

        for book in cart['books']:
            #associate book to account
            pass
    except Exception as e:
        print(e)
        return None