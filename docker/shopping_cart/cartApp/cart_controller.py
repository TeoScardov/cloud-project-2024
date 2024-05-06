import json

from flask import Blueprint
from flask import jsonify, request
from . import database, call_service, utility

cart = Blueprint('cart', __name__)


@cart.route("/health")
def health():
    return jsonify(
        status="UP"
    )


@cart.route("/addProduct", methods=["POST"])
def add_product():
    """
    Add the provided quantity of a product to a cart. Where an item already exists in the cart, the quantities will
    be summed.

    it does not depend on user being logged in or not however in the database there is a user_id field that will get set
    as the user logs in and if a cart has a user_id it won't get deleted after expiry.
    """
    try:
        request_payload = request.json
    except (ValueError, TypeError) as e:
        return {
            "statusCode": 400,
            "headers": utility.get_headers(None),
            "body": json.dumps({"message": "No Request payload"}),
        }
    product_id = request_payload["product_id"]
    cart_id = request_payload["cart_id"]
    user_id = None
    user_cart_id = None
    try:
        product = call_service.get_product_from_external_service(product_id)
    except Exception as e:
        return {
            "statusCode": 404,
            "headers": utility.get_headers(cart_id=cart_id),
            "body": json.dumps({"message": str(e)}),
        }

    if 'Authorization' in request.headers:
        try:
            user_id = call_service.authenticate_user_with_jwt(request.headers['Authorization'])
        except Exception as e:
            return {
                "statusCode": 404,
                "headers": utility.get_headers(cart_id=cart_id),
                "body": json.dumps({"message": str(e)}),
            }
    if user_id:
        user_cart_id = database.check_for_user_cart(user_id)

    if not user_cart_id:
        if cart_id:
            if database.check_cart_id(cart_id):
                database.renew_cart_expiry(cart_id, user_id)
                current_cart = database.add_item(cart_id, product, user_id)
            else:
                return {
                    "statusCode": 404,
                    "headers": utility.get_headers(cart_id=cart_id),
                    "body": json.dumps({"message": "cart_id is not valid"}),
                }
        else:
            cart_id = database.insert_cart(0, user_id)
            current_cart = database.add_item(cart_id, product, user_id)
    else:
        if cart_id:
            if cart_id == user_cart_id:
                database.renew_cart_expiry(user_cart_id, user_id)
                current_cart = database.add_item(user_cart_id, product, user_id)
            elif database.check_cart_id(cart_id):
                database.renew_cart_expiry(cart_id, user_id)
                database.add_item(cart_id, product, user_id)
                current_cart = database.merge_carts(user_id)
            else:

                return {
                    "statusCode": 404,
                    "headers": utility.get_headers(cart_id),
                    "body": json.dumps({"message": "cart_id is not valid", "user_cart_id": str(user_cart_id)}),
                }
        else:
            database.renew_cart_expiry(user_cart_id, user_id)
            current_cart = database.add_item(user_cart_id, product, user_id)

    return {
        "statusCode": 200,
        "headers": utility.get_headers(cart_id),
        "body": json.dumps(
            {"productId": str(product_id), "message": "product added to cart",
             "cart_id": str(current_cart.id), "total": current_cart.total,
             "product": {"name": product["name"], "price": product["price"]}}
        ),
    }


@cart.route("/removeProduct", methods=["DELETE"])
def remove_product():
    try:
        request_payload = request.json
    except (ValueError, TypeError) as e:
        return {
            "statusCode": 400,
            "headers": utility.get_headers(None),
            "body": json.dumps({"message": "No Request payload"}),
        }
    product_id = request_payload["product_id"]
    cart_id = request_payload["cart_id"]
    user_id = None
    user_cart_id = None
    try:
        product = call_service.get_product_from_external_service(product_id)
    except Exception as e:
        return {
            "statusCode": 404,
            "headers": utility.get_headers(cart_id=cart_id),
            "body": json.dumps({"message": str(e)}),
        }

    if 'Authorization' in request.headers:
        try:
            user_id = call_service.authenticate_user_with_jwt(request.headers['Authorization'])
        except Exception as e:
            return {
                "statusCode": 404,
                "headers": utility.get_headers(cart_id=cart_id),
                "body": json.dumps({"message": str(e)}),
            }
    if user_id:
        user_cart_id = database.check_for_user_cart(user_id)

    if not user_cart_id:
        if cart_id:
            if database.check_cart_id(cart_id):
                database.renew_cart_expiry(cart_id, user_id)
                current_cart = database.delete_item(cart_id, product, user_id)
            else:
                return {
                    "statusCode": 404,
                    "headers": utility.get_headers(cart_id=cart_id),
                    "body": json.dumps({"message": "cart_id is not valid", "user_cart_id": str(user_cart_id)}),
                }
        else:
            return {
                "statusCode": 404,
                "headers": utility.get_headers(cart_id=cart_id),
                "body": json.dumps({"message": "cart_id not provided "}),
            }
    else:
        if cart_id:
            if cart_id == user_cart_id:
                database.renew_cart_expiry(user_cart_id, user_id)
                current_cart = database.delete_item(user_cart_id, product, user_id)
            elif database.check_cart_id(cart_id):
                database.renew_cart_expiry(cart_id, user_id)
                database.delete_item(cart_id, product, user_id)
                current_cart = database.merge_carts(user_id)
            else:
                return {
                    "statusCode": 404,
                    "headers": utility.get_headers(cart_id=cart_id),
                    "body": json.dumps({"message": "cart_id is not valid", "user_cart_id": str(user_cart_id)}),
                }
        else:
            return {
                "statusCode": 404,
                "headers": utility.get_headers(cart_id=cart_id),
                "body": json.dumps({"message": "cart_id not provided"}),
            }

    return {
        "statusCode": 200,
        "headers": utility.get_headers(cart_id),
        "body": json.dumps(
            {"productId": str(product_id), "message": "product deleted from the cart",
             "cart_id": str(current_cart.id), "total": current_cart.total,
             "product": {"name": product["name"], "price": product["price"]}}
        ),
    }


@cart.route("/show_cart", methods=["GET"])
def show_cart():
    cart_id = request.args.get('cart_id')
    if cart_id:
        if database.check_cart_id(cart_id):
            current_cart = database.renew_cart_expiry(cart_id, None)
            cart_items = database.get_cart_items_by_cart_id(cart_id)
            response_data = {"cart_id": str(current_cart.id), "total": current_cart.total, "items": cart_items}
            return {
                "statusCode": 200,
                "headers": utility.get_headers(cart_id),
                "body": json.dumps(response_data),
            }
    else:
        return {
            "statusCode": 404,
            "headers": utility.get_headers(cart_id=cart_id),
            "body": json.dumps({"message": "cart_id needed"}),
        }


@cart.route("/removeCart", methods=["DELETE"])
def remove_cart():
    try:
        request_payload = request.json
    except (ValueError, TypeError) as e:
        return {
            "statusCode": 400,
            "headers": utility.get_headers(None),
            "body": json.dumps({"message": "No Request payload"}),
        }
    cart_id = request_payload["cart_id"]
    user_id = None
    user_cart_id = None

    if 'Authorization' in request.headers:
        try:
            user_id = call_service.authenticate_user_with_jwt(request.headers['Authorization'])
        except Exception as e:
            return {
                "statusCode": 404,
                "headers": utility.get_headers(cart_id=cart_id),
                "body": json.dumps({"message": str(e)}),
            }
    else:
        return {
            "statusCode": 404,
            "headers": utility.get_headers(cart_id=cart_id),
            "body": json.dumps({"message": "invalid request! no auth"}),
        }

    user_cart_id = str(database.check_for_user_cart(user_id))

    if not user_cart_id:
        return {
            "statusCode": 404,
            "headers": utility.get_headers(cart_id=cart_id),
            "body": json.dumps({"message": "this user doesn't have cart to delete!"}),
        }
    else:
        if cart_id:
            if cart_id == user_cart_id:
                database.delete_cart(user_cart_id, user_id)
            else:
                return {
                    "statusCode": 404,
                    "headers": utility.get_headers(cart_id=cart_id),
                    "body": json.dumps({"message": "request is not valid"}),
                }
        else:
            database.delete_cart(user_cart_id, user_id)

    return {
        "statusCode": 200,
        "headers": utility.get_headers(user_cart_id),
        "body": json.dumps(
            {"message": "cart deleted"}
        ),
    }
