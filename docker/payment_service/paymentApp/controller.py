def perform_payment(request):

    try:
        amount = request.get_json()['amount']
        card = request.get_json()['card']
        cvv = request.get_json()['cvv']
        expiration = request.get_json()['expiration']
        billing_address = request.get_json()['billing_address']
        status = "APPROVED"

        return status
    
    except:
        return None
