from http import HTTPStatus as _HTTPStatus
from typing import Any


def _make_error(http_status, code: str, message: str | None = None):
    try:
        http_status = http_status[0]
    except Exception:
        pass

    payload = {
        'status': 'error',
        'code': code,
    }

    if message is not None:
        payload['message'] = message

    return payload, http_status


# General

INVALID_REQUEST = _make_error(
    _HTTPStatus.BAD_REQUEST,
    'general/invalid_request',
)

NOT_FOUND = _make_error(
    _HTTPStatus.NOT_FOUND,
    'general/not_found',
)

def invalid_argument(argname: str) -> tuple[Any, int]:
    return _make_error(
        _HTTPStatus.UNPROCESSABLE_ENTITY,
        'general/invalid_argument',
        message=f'Invalid argument: {argname}',
    )

# Login

INVALID_DETAILS = _make_error(
    _HTTPStatus.UNAUTHORIZED,
    'login/invalid_details',
)

NO_AUTHORIZATION = _make_error(
    _HTTPStatus.UNAUTHORIZED,
    'login/no_authorization',
)

INVALID_AUTHORIZATION = _make_error(
    _HTTPStatus.UNAUTHORIZED,
    'login/invalid_authorization',
)

UNAUTHORIZED = _make_error(
    _HTTPStatus.UNAUTHORIZED,
    'login/unauthorized',
    "You are logged in but the resource you're trying to access isn't available to you",
)

# Transactions

NO_BALANCE = _make_error(
    _HTTPStatus.BAD_REQUEST,
    'transaction/no_balance',
    'Not enough balance to make the transaction',
)

INVALID_IBAN = _make_error(
    _HTTPStatus.BAD_REQUEST,
    'transaction/invalid_iban',
    'Recipient IBAN is invalid',
)


# Success

def success(http_status: Any = _HTTPStatus.OK, /, **kargs):
    try:
        http_status = http_status[0]
    except Exception:
        pass

    return dict(kargs, status='success'), http_status

# Schemas

from marshmallow import Schema, fields, validate

class ErrorSchema(Schema):
    status = fields.Str(default='error', validate=validate.Equal('error'))
    code = fields.Str()
    message = fields.Str(required=False)

class SuccessSchema(Schema):
    status = fields.Str(default='success', validate=validate.Equal('success'))

# smorest

def abort(result: tuple[Any, int]):
    try:
        from flask_smorest import abort as _abort
        _abort(result[1], response=result)
    except ImportError:
        return result
