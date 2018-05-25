from .Exceptions import BadRequest
from flask import jsonify

def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response