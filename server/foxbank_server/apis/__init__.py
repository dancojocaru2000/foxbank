from flask import Flask
from flask_smorest import Api

from .accounts import bp as acc_bp
from .login import bp as login_bp

def init_apis(app: Flask):
    api = Api(app, spec_kwargs={
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
