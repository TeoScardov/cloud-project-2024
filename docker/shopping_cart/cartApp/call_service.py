
from .config import USER_SERVICE_URL
from .config import PRODUCT_SERVICE_URL


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

    return {
        'product_id': '94ff3b8b-56bf-453d-af20-a2fd78feae55',
        'name': '12 rules for life',
        'price': 12
    }


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
    return 2
