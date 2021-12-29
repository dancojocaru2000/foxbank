#! /usr/bin/env python3
from foxbank_server import create_app

app = create_app()
# api = Api(app)
# CORS(app)
# db.init_app(app)

# from login import login
# app.register_blueprint(login, url_prefix='/login')

# from bank_accounts import blueprint as ba_bp, namespace as ba_ns
# app.register_blueprint(ba_bp, url_prefix='/accounts')

# accounts_ns = api.add_namespace(ba_ns, '/accounts')

if __name__ == '__main__':
    app.run(debug=True)
