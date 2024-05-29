from flask import Blueprint
from flask import request
from flask import jsonify, make_response
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

    if payment.status_code != 200:
        return make_response(jsonify({
            "message": "Payment failed",
            "status": "DECLINED",
            "error": str(payment)
        }), 500)
    
    else:
        return make_response(jsonify({
            "message": "Payment successful",
            "status": "APPROVED"
        }), 200) 