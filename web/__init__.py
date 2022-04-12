from flask import Flask
from os import path
from .models import Person


def create_app():
    app = Flask('HTTP Playground')
    app.debug = True
    create_db()
    return app


def create_db():
    db_uri = 'data.db'
    if not path.exists(db_uri):
        from .DBManager import DBManager
        db = DBManager(db_uri)
        _ = db.connect()
        _.close()
        db.create_tables({'Person': Person})






