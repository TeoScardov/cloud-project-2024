def perform_payment(request):

    try:
        total = request.get_json().get('cart').get('total')
        card = request.get_json().get('cc')
        cvv = request.get_json().get('cvv')
        expiration = request.get_json().get('expiredate')
        billing_address = request.get_json().get('billing_address')
        status = "APPROVED"

        return status
    
    except Exception as e:
        return e
