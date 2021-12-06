from http import HTTPStatus
from functools import wraps

def no_content(fn):
    @wraps(fn)
    def wrapper(*args, **kargs):
        result = fn(*args, **kargs)
        if result is None:
            return None, HTTPStatus.NO_CONTENT
        else:
            return result
    return wrapper
