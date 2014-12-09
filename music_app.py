# -*- coding: utf-8 -*-
import os
from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from sqlite3 import dbapi2 as sqlite3

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '/data/player.sqlite3'),
    DEBUG=True,
))
app.config.from_envvar('APP_SETTINGS', silent=True)

from player.models import AccessToken, User, Playlist, Track, db as app_db
from player.views import mod as player_views

db = app_db

# register views defined for this app
app.register_blueprint(player_views)

if __name__ == "__main__":
    app.run()
