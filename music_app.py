# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '/data/player.sqlite3'),
    DEBUG=True,
))
app.config.from_envvar('APP_SETTINGS', silent=True)

db = SQLAlchemy(app)

# register views defined for this app
from player.views import mod as playlistModule
app.register_blueprint(playlistModule)

if __name__ == "__main__":
    app.run()
