from flask import Flask
from .apis import init_apis

class Config:
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    init_db(app)
    init_cors(app)
    init_apis(app)

    return app

def init_cors(app):
    from flask_cors import CORS
    cors = CORS()
    cors.init_app(app)

def init_db(app):
    from .db import init_app
    init_app(app)
