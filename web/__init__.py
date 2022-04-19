from flask import Flask
from os import path
from .models import Person
from .api import api

DB_URI = 'data.db'


def create_app():
    '''
    Using python-dotenv, loading configuration from .flaskenv
    :return: Flask app object
    '''
    app = Flask('HTTP Playground')
    app.register_blueprint(api, url_prefix='/')
    create_db()
    app.register_error_handler(500, server_error)
    app.register_error_handler(406, invalid_data)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(404, not_found)
    app.register_error_handler(400, bad_request)
    return app


def create_db():
    if not path.exists(DB_URI):
        from .DBManager import DBManager
        db = DBManager(DB_URI)
        _ = db.connect()
        _.close()
        db.create_tables({'Person': Person})


def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code, 'Content-Type': 'application/json'}


def server_error(e):
    return template(data=str(e), code=500), 500


def invalid_data(e):
    return template(data=str(e), code=406), 406


def method_not_allowed(e):
    return template(data=str(e), code=405), 405


def not_found(e):
    return template(data=str(e), code=404), 404


def bad_request(e):
    return template(data=str(e), code=400), 400
