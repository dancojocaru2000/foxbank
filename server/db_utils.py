from functools import wraps

import db
import models

def get_db(fn):
    @wraps(fn)
    def wrapper(*args, **kargs):
        return fn(db.get(), *args, **kargs)
    return wrapper

@get_db
def get_user(db: db.get_return, username: str|None = None, user_id: int|None = None) -> models.User | None:
    cur = db.cursor()
    if username is not None:
        cur.execute('select * from users where username=?', (username,))
    elif user_id is not None:
        cur.execute('select * from users where id=?', (user_id,))
    else:
        raise Exception('Neither username or user_id passed')
    result = cur.fetchone()
    if result is None:
        return None
    return models.User.from_query(result)
