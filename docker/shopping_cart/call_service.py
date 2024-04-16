
from .database import get_product_by_id
# from config import USER_SERVICE_URL


def get_product_from_external_service(product_id):
    """
    Call product API to retrieve product details
    """
    # response = requests.get(PRODUCT_SERVICE_URL + f"/product/{product_id}")
    # try:
    #     response_dict = response.json()["product"]
    # except KeyError:
    #     logger.warn("No product found with id %s", product_id)
    #     raise NotFoundException
    #
    # return response_dict
    product = get_product_by_id(product_id)
    if product is not None:
        return {
            'product_id': product.id,
            'name': product.name,
            'price': product.price
        }
    else:
        raise Exception('Product not found')


def authenticate_user_with_jwt(auth_header):
    # token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else None
    #
    # if not token:
    #     raise Exception('Invalid Authorization header format')
    #
    # # Make a request to the authentication API
    # response = requests.post(USER_SERVICE_URL + f"/authenticate", json={'token': token})
    #
    # if response.status_code == 200:
    #     # Token is valid, extract user_id from the response
    #     user_id = response.json().get('user_id')
    #     return user_id
    # else:
    #     # Token is not valid, return None
    #     return None
    # return auth_header
    return None
