from flask import Blueprint

account = Blueprint('cart', __name__)

from . import cart_controller
