from flask import Flask
from os import path
from .models import Person
from .api import api

DB_URI = 'data.db'

def create_app():
    app = Flask('HTTP Playground')
    app.debug = True
    app.register_blueprint(api, url_prefix='/')
    create_db()
    return app


def create_db():
    if not path.exists(DB_URI):
        from .DBManager import DBManager
        db = DBManager(DB_URI)
        _ = db.connect()
        _.close()
        db.create_tables({'Person': Person})






