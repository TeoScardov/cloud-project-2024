class PurchaseController:
    def __init__(self):
        ...

    def getUserToken(self, token):

        return {
            'status': 'success',
            'getUserToken': token
        }

    def commitPurchase(self, id):

        return {
            'status': 'success',
            'commitPurchase': id
        }

    def addPurchasedProduct(self, purchases):
        return {
            'status': 'success',
            'addPurchasedProduct': purchases
        }
    
    
    def placeOrder(self, user_id, products):
        return {
            'status': 'success',
            'placeOrder': user_id,
            'products': products
        }