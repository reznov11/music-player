# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI= "sqlite:///%s" % os.path.join(app.root_path, 'data/player.sqlite3'),
    DEBUG=True,
    PRECACHED_ALBUM_DATA= os.path.join(app.root_path, 'data/precached_album_data.json'),
    PRECACHED_ARTIST_DATA= os.path.join(app.root_path, 'data/precached_artist_data.json'),
    PRECACHED_TRACK_DATA= os.path.join(app.root_path, 'data/precached_track_data.json'),
))
app.config.from_envvar('APP_SETTINGS', silent=True)

db = SQLAlchemy(app)

# register views defined for this app
from player.views import *

if __name__ == "__main__":
    app.run()
