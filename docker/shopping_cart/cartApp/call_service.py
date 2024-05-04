import requests
import json
from .config import USER_SERVICE_URL
from .config import PRODUCT_SERVICE_URL



def get_product_from_external_service(product_id):
    """
    # Call product API to retrieve product details
    # """
    api_url = PRODUCT_SERVICE_URL + '/get-book-details'

    # # Assuming headers you want to include in the request
    # json_data = {
    #     "id": product_id
    # }
    #
    # # Convert the dictionary to JSON string
    # json_string = json.dumps(json_data)
    #
    # try:
    #     # Sending the POST request with JSON data and headers
    #     response = requests.post(api_url, json=json_string)
    #
    #     # Checking if the request was successful (status code 200)
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         # If the request was not successful, raise an exception
    #         response.raise_for_status()
    # except requests.exceptions.RequestException as e:
    #     # Handling any exceptions that might occur during the request
    #     print("Error:", e)
    #     return None

    return {
        'product_id': '94ff3b8b-56bf-453d-af20-a2fd78feae55',
        'name': '12 rules for life',
        'price': 12
    }


def authenticate_user_with_jwt(auth_header):
    token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else None
    if not token:
        raise Exception('Invalid Authorization header format')

    # Assuming the URL of the API you want to call
    api_url = USER_SERVICE_URL + '/authenticate'

    # Assuming headers you want to include in the request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_header
        # Add other headers as needed
    }

    try:
        # Sending the POST request with JSON data and headers
        response = requests.post(api_url, headers=headers)

        # Checking if the request was successful (status code 200)
        if response.status_code == 200:
            # Parsing the JSON response
            response_json = response.json()

            # Returning the JSON response
            return response_json.get('username')
        else:
            # If the request was not successful, raise an exception
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Handling any exceptions that might occur during the request
        print("Error:", e)
        return None

