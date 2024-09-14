from flask import Flask
from routers.api_auth import api_auth
from routers.api_documents import api_documents


API_VERSION_PREFIX = '/api/v1'

def register_route(app: Flask):
    app.register_blueprint(api_auth, url_prefix=API_VERSION_PREFIX)
    app.register_blueprint(api_documents, url_prefix=API_VERSION_PREFIX)
