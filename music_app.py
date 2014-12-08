# -*- coding: utf-8 -*-
import os
from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from sqlite3 import dbapi2 as sqlite3
import pdb
app = Flask(__name__)

# app.config.from_pyfile('config.py', silent=True)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'player.sqlite3'),
    DEBUG=True,
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


from player.models import AccessToken, User, Playlist, Track, db as app_db
from player.views import mod as player_views

db = app_db

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    return SQLAlchemy(app)

def init_db():
    """Initializes the database."""
    db = get_db()
    print db
    pdb.set_trace()
    db.create_all()


# @app.cli.command('initdb')
# def initdb_command():
#     """Creates the database tables."""
#     init_db()
#     print('Initialized the database.')



# register views defined for this app
app.register_blueprint(player_views)

if __name__ == "__main__":
    app.run()
