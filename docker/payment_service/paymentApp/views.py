from flask import Blueprint
from flask import request
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required

from paymentApp.controller import perform_payment

blueprint = Blueprint('payment', __name__)

@blueprint.route('/', methods=['GET'])
def health():
    """
    This function is used to check the health of the purchase service.
    It returns a message indicating that the service is up and running.
    ---
    responses:
        200:
            description: Purchase service is up and running
    """

    return "Payment service is up and running &#128640;", 200

@blueprint.route('/', methods=['POST'])
@jwt_required()
def pay():
    """
    Perform a payment
    ---
    parameters:
    
        - name: purchase_data
          in: body
          required: true
          schema:
            type: object
            properties:
                total:
                    type: number
                    description: Total amount to be paid
                cc:
                    type: string
                    description: Credit card number
                cvv:
                    type: string
                    description: CVV number
                expiredate:
                    type: string
                    description: Expiration date
                billing_address:
                    type: string
                    description: Billing address
        
    responses:
        200:
            description: Payment successful
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Payment successful
                    status:
                        type: string
                        description: APPROVED
        500:
            description: Payment failed
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Payment failed
                    status:
                        type: string
                        description: REJECTED
                    error:
                        type: string
                        description: Error message   
    """

    payment = perform_payment(request)

    if payment.status_code != 200:
        return make_response(jsonify({
            "message": "Payment failed",
            "status": "REJECTED",
            "error": str(payment)
        }), 500)
    
    else:
        return make_response(jsonify({
            "message": "Payment successful",
            "status": "APPROVED"
        }), 200) 