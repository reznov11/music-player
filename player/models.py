import json
from flask.ext.sqlalchemy import SQLAlchemy
from music_app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class AccessToken(db.Model):
    @classmethod
    def from_json(cls, data):
        token_dict = json.loads(data)
        return cls(
            token_dict['access_token'],
            token_dict['token_type'],
            token_dict['expires_in'],
            token_dict['refresh_token'])


    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255))
    token_type = db.Column(db.String(50))
    expires_in = db.Column(db.Integer)
    refresh_token = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                    backref=db.backref('access_token', lazy='dynamic'))

    def __init__(self, access_token, token_type, expires_in, refresh_token):
        self.access_token = access_token 
        self.token_type = token_type
        self.expires_in = expires_in
        self.refresh_token = refresh_token


tracks = db.Table('tracks',
    db.Column('track_id', db.Integer, db.ForeignKey('track.id')),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')))

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User',
                backref=db.backref('playlists', lazy='dynamic'))

    tracks = db.relationship('Track', secondary=tracks,
            backref=db.backref('playlists', lazy='dynamic'))

    def __init__(self, title, user):
        self.title = title
        self.user = user

    def __repr__(self):
        return '<Playlist %r>' % (self.title)


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=True)
    uri = db.Column(db.String(50), unique=True)
    track_id = db.Column(db.String(140), unique=True)

    def __init__(self, track_id, title, uri):
        self.title = title
        self.track_id = track_id
        self.uri = uri

    def __repr__(self):
        return '<Track %r>' % (self.title)