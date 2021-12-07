from http import HTTPStatus as _HTTPStatus

def _make_error(http_status, code: str):
    try:
        http_status = http_status[0]
    except Exception:
        pass

    return {
        'status': 'error',
        'code': code,
    }, http_status

# General

INVALID_REQUEST = _make_error(
    _HTTPStatus.BAD_REQUEST,
    'general/invalid_request',
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

# Success

def success(http_status=_HTTPStatus.OK, /, **kargs):
    try:
        http_status = http_status[0]
    except Exception:
        pass

    return dict(kargs, status='success'), http_status
