from flask import make_response, jsonify


def perform_payment(request):

    print(request.get_json(), flush=True)

    try:
        total = request.get_json().get('total')
        card = request.get_json().get('cc')
        cvv = request.get_json().get('cvv')
        expiration = request.get_json().get('expiredate')
        billing_address = request.get_json().get('billing_address')
        status = "APPROVED"
        
        payment_data = {
            "total": total,
            "card": card,
            "cvv": cvv,
            "expiration": expiration,
            "billing_address": billing_address,
            "status": status
        }

        return make_response(jsonify({
            "message": "Payment successful",
            "status": "APPROVED"
        }), 200)
    
    except Exception as e:
        return make_response(jsonify({
            "message": "Payment failed",
            "status": "REJECTED",
            "error": str(e)
        }), 500)
