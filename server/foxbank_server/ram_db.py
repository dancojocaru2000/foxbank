from datetime import datetime, timedelta
from uuid import uuid4

USED_TOKENS = set()
LOGGED_IN_USERS: dict[str, (int, datetime)] = {}

def login_user(user_id: int) -> str:
    '''
    Creates token for user
    '''
    token = str(uuid4())
    while token in USED_TOKENS:
        token = str(uuid4())
    if len(USED_TOKENS) > 10_000_000:
        USED_TOKENS.clear()
        for token in LOGGED_IN_USERS:
            USED_TOKENS.add(token)
    USED_TOKENS.add(token)
    LOGGED_IN_USERS[token] = user_id, datetime.now()
    return token

def logout_user(token: str):
    if token in LOGGED_IN_USERS:
        del LOGGED_IN_USERS[token]

def get_user(token: str) -> int | None:
    if token not in LOGGED_IN_USERS:
        return None

    user_id, login_date = LOGGED_IN_USERS[token]
    time_since_login: timedelta = datetime.now() - login_date
    if time_since_login.total_seconds() > (60 * 30): # 30 mins
        del LOGGED_IN_USERS[token]
        return None
    return user_id
