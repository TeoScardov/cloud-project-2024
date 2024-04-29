from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import jwt_required

from paymentApp.controller import perform_payment

blueprint = Blueprint('payment', __name__)

@blueprint.route('/', methods=['GET'])
def health():
    return jsonify(
        status="UP"
    )

@blueprint.route('/', methods=['POST'])
@jwt_required()
def pay():

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