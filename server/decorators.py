from flask import request
from http import HTTPStatus
from functools import wraps
import ram_db
import returns

def no_content(fn):
    '''
    Allows a Flask route to return None, which is converted into
    HTTP 201 No Content.
    '''
    @wraps(fn)
    def wrapper(*args, **kargs):
        result = fn(*args, **kargs)
        if result is None:
            return None, HTTPStatus.NO_CONTENT
        else:
            return result
    return wrapper

def ensure_logged_in(token=False, user_id=False):
    '''
    Ensure the user is logged in by providing an Authorization: Bearer token
    header.

    @param token whether the token should be supplied after validation
    @param user_id whether the user_id should be supplied after validation
    @return decorator which supplies the requested parameters
    '''
    def decorator(fn):
        pass_token = token
        pass_user_id = user_id
        @wraps(fn)
        def wrapper(*args, **kargs):
            token = request.headers.get('Authorization', None)
            if token is None:
                return returns.NO_AUTHORIZATION
            if not token.startswith('Bearer '):
                return returns.INVALID_AUTHORIZATION
            token = token[7:]
            user_id = ram_db.get_user(token)
            if user_id is None:
                return returns.INVALID_AUTHORIZATION

            if pass_user_id and pass_token:
                return fn(user_id=user_id, token=token, *args, **kargs)
            elif pass_user_id:
                return fn(user_id=user_id, *args, **kargs)
            elif pass_token:
                return fn(token=token, *args, **kargs)
            else:
                return fn(*args, **kargs)
        return wrapper
    return decorator
