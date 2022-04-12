from flask import Flask
from os import path
import sqlite3
from .people import Person


def createApp():
    app = Flask('HTTP Playground')
    app.debug = True
    createDB()
    return app


def createDB():
    db_uri = 'data.db'
    if not path.exists(db_uri):
        from db import DBManager
        db = DBManager(db_uri)
        _ = db.connect()
        db.create_tables({'Person': Person})






