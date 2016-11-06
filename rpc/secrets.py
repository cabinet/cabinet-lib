import os
import base64

DEFAULT_ENTROPY = 32  # number of bytes to return by default


def token_urlsafe(nbytes=None):
    """
    In the future, it can be replaced by secrets.token_urlsafe
    Reference: https://docs.python.org/3/library/secrets.html
    """
    if nbytes is None:
        nbytes = DEFAULT_ENTROPY
    token = os.urandom(nbytes)
    return base64.urlsafe_b64encode(token).rstrip(b'=').decode('ascii')
