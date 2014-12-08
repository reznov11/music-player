import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///%s/player.sqlite3" % _basedir
