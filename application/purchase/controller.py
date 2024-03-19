import requests
from models import PaymentDao, PurchaseDao, PurchaseItemDao

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