from functools import wraps
from flask import request


def authenticate(f_check_token):
    def auth(f):
        @wraps(f)
        def _f(*args, **kwargs):
            client_token = request.headers.get('token')
            if not f_check_token(client_token):
                return {
                    'success': False,
                    'error': {
                        'code': 401,
                        'message': 'Unauthorized Token'
                    }
                }
            return f(*args, **kwargs)
        return _f
    return auth
