from flask import Blueprint
from flask import request
from flask import jsonify

payment_bp = Blueprint('payment', __name__)

@payment_bp.route("/health")
def health():
    return jsonify(
        status="UP"
    )

@payment_bp.route('/pay', methods=['GET'])
def payment():
    #do payment process
    return jsonify({
            'status': 'success',
            'payment': 'Gormiti'
        }), 200
