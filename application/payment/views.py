from flask import Blueprint
from flask import request
from flask import jsonify
from controller import perform_payment

blueprint = Blueprint('payment', __name__)

@blueprint.route('/', methods=['GET'])
def health():
    return jsonify(
        status="UP"
    )

@blueprint.route('/', methods=['POST'])
def pay():

    if request.authorization is None:
        return jsonify({
            'status': 'error',
            'authenticate': 'Not authenticated'
        }), 401
    else:

        payment = perform_payment(request)

        if payment is None:
            return jsonify({
                'status': 'error',
                'message': 'Payment failed'
            }), 500
        
        else:
            return jsonify({
                "message": "Payment successful",
                "status": payment,

            }), 200