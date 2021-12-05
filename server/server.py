from flask import Flask
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)
db.init_app(app)

from login import login
app.register_blueprint(login, url_prefix='/login')

if __name__ == '__main__':
    app.run()
