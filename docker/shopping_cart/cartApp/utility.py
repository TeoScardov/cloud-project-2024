import datetime
import os

from flask import jsonify

HEADERS = {
    #"Access-Control-Allow-Origin": #os.environ.get("ALLOWED_ORIGIN"),
    #"Access-Control-Allow-Headers": "Content-Type",
    #"Access-Control-Allow-Methods": "OPTIONS,POST,GET",
    #"Access-Control-Allow-Credentials": True,
}


def generate_ttl(days=1):
    """
    Generate epoch timestamp for number days in future
    """
    future = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=days)
    return future


#

def create_response(cart_id, json_data, status_code):
    response = jsonify(json_data)
    response.status_code = status_code
    response.mimetype = 'application/json'

    for header, value in HEADERS.items():
        response.headers[header] = value

    response.set_cookie(
        key='cartId',
        value=cart_id,
        max_age=60 * 60 * 24,  # 1 day in seconds
        secure=True,
        httponly=True,
        path='/'
    )

    return response
