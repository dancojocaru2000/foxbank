from functools import wraps
from flask import Blueprint, request

from pyotp import TOTP

import db_utils
from decorators import no_content
import models
import ram_db
import returns

login = Blueprint('login', __name__)

@login.post('/')
def make_login():
    try:
        username = request.json['username']
        code = request.json['code']
    except (TypeError, KeyError):
        return returns.INVALID_REQUEST

    user: models.User | None = db_utils.get_user(username=username)
    if user is None:
        return returns.INVALID_DETAILS

    otp = TOTP(user.otp)
    if not otp.verify(code, valid_window=1):
        return returns.INVALID_DETAILS

    token = ram_db.login_user(user.id)
    return returns.success(token=token)

def ensure_logged_in(token=False, user_id=False):
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

@login.post('/logout')
@ensure_logged_in(token=True)
@no_content
def logout(token: str):
    ram_db.logout_user(token)

@login.get('/whoami')
@ensure_logged_in(user_id=True)
def whoami(user_id: int):
    user: models.User | None = db_utils.get_user(user_id=user_id)
    if user is not None:
        user = user.to_json()

    return returns.success(user=user)