from functools import wraps
from flask import Blueprint, request

from pyotp import TOTP

import db_utils
from decorators import no_content, ensure_logged_in, user_id, token
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

@login.post('/logout')
@ensure_logged_in
@no_content
def logout():
    ram_db.logout_user(token)

@login.get('/whoami')
@ensure_logged_in
def whoami():
    user: models.User | None = db_utils.get_user(user_id=user_id)
    if user is not None:
        user = user.to_json()

    return returns.successs(user=user)

