from flask import Flask

import db

app = Flask(__name__)
db.init_app(app)

@app.get('/')
def root():
    return 'Hello from FoxBank!'
