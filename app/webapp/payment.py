from flask import Blueprint
from flask import request
from flask import jsonify

from .Payment.PaymentController import PaymentController

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment/<payment_id>', methods=['GET'])
def payment():
    payment = PaymentController()

    #do payment process
    
    return jsonify(payment.pay("Gormiti")), 200
