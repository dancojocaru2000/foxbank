import sqlite3

from flask import current_app, g

DB_FILE = './data/db.sqlite'

get_return = sqlite3.Connection

def get() -> get_return:
    if 'db' not in g:
        g.db = sqlite3.connect(
            DB_FILE,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close(e=None):
    db = g.pop('db', None)

    if db:
        db.close()

def init():
    db = get()

    with current_app.open_resource('init.sql') as f:
        db.executescript(f.read().decode('utf8'))
        db.commit()

def init_app(app):
    app.teardown_appcontext(close)

    import os.path
    if not os.path.exists(DB_FILE):
        with app.app_context():
            init()
