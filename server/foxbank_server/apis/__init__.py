from flask import Flask
from flask_smorest import Api

from .accounts import bp as acc_bp
from .login import bp as login_bp
from .transactions import bp as transactions_bp

class ApiWithErr(Api):
    def handle_http_exception(self, error):
        if error.data and error.data['response']:
            return error.data['response']
        return super().handle_http_exception(error)

def init_apis(app: Flask):
    api = ApiWithErr(app, spec_kwargs={
        'title': 'FoxBank',
        'version': '1',
        'openapi_version': '3.0.0',
        'components': {
            'securitySchemes': {
                'Token': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'bearerFormat': 'Token ',
                }
            }
        },
    })
    api.register_blueprint(login_bp, url_prefix='/login')
    api.register_blueprint(acc_bp, url_prefix='/accounts')
    api.register_blueprint(transactions_bp, url_prefix='/transactions')
