from functools import wraps
from flask import request
from flask_jsonrpc.exceptions import InvalidCredentialsError


def authenticate(f, f_check_auth):
    @wraps(f)
    def _f(*args, **kwargs):
        token = request.headers.get('token')
        if not f_check_auth(token):
            raise InvalidCredentialsError()
        return f(*args, **kwargs)
    return _f
