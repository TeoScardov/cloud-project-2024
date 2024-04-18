from requests.models import Response as requestsResponse
from flask.wrappers import Response as flaskResponse
from flask import jsonify, make_response

def toFlaskResponse(response: requestsResponse)->flaskResponse:

    flask_response = make_response(jsonify(response.json()), response.status_code, response.headers.items())

    return flask_response