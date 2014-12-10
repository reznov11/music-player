from __future__ import absolute_import
from flask import request, Response, jsonify

from lib.spotify.client import Client as spotify_api_client
from music_app import db, app

from . models import *

@app.route('/', methods = ['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(endpoints=func_list)

@app.route("/playlists", methods=['GET', 'POST'])
def get_or_create_playlists():
    """
    `POST` Creates a playlist

    `GET` Returns a list of playlists belonging to the current user.

    If the request method is POST, a new playlist will be
    created from the posted data. The response is a JSON
    representation of the created playlist object

    If the request method is GET, all playlists belonging to
    the current user are retrieved and returned as a JSON
    list
    """
    user = User.query.get(1)
    if request.method == 'POST':
        # create playlist
        data = request.get_json()
        title = data.get('title', None)

        if title is None:
            return Response('title cannot be empty', status=403)

        pl = Playlist(title, user)
        db.session.add(pl)
        db.session.commit()
        return jsonify(
            title=pl.title,
            user_id=pl.user_id,
            tracks=pl.tracks)
    else:
        # return all playlists belonging to current user  
        playlists = Playlist.query.filter_by(user_id=user.id).all()
        return jsonify(playlists=[p.serialize for p in playlists])


@app.route("/playlists/<playlist_id>", methods=['GET', 'PUT', 'DELETE'])
def view_or_update_playlist(playlist_id):
    """
    `GET` Fetches a playlist with the provided database ID. If the 
    playlist is not found, a 404 response is returned. 

    `PUT` Updates the title for existing playlist

    `DELETE` Deletes playlist with provided ID 
    """
    pl = Playlist.query.filter_by(id=playlist_id, user_id=1).first_or_404()

    if request.method == 'DELETE':
        db.session.delete(pl)
        db.session.commit()
        return Response('', status=200)
    elif request.method == 'PUT':
        # update playlist
        data = request.get_json()
        title = data['title']
        
        # playlist title already used
        if pl.title == title:
            return Response('playlist with this title already exists', status=403)

        pl.title = title
        db.session.commit()
    return jsonify(
            title=pl.title,
            user_id=pl.user_id,
            tracks=[t.serialize for t in pl.tracks])


@app.route("/playlists/<playlist_id>/add_track", methods=['POST'])
def add_track_to_playlist(playlist_id):
    """
    `POST` Adds track with provided database ID to playlist with specified ID
    """
    pl = Playlist.query.filter_by(id=playlist_id, user_id=1).first_or_404()
    data = request.get_json()
    t_id = data['id']
    track = Track.query.get_or_404(t_id)

    pl.tracks.append(track)
    db.session.commit()
    return Response('', status=201)

@app.route("/playlists/<playlist_id>/remove_track", methods=['DELETE'])
def remove_track_to_playlist(playlist_id):
    """
    `DELETE` Removes track with provided database ID to playlist with specified ID
    """
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=1).first_or_404()

    data = request.get_json()
    pk = data.get('pk', None)

    track = Track.query.get(pk)
    if track is None:
        return Response("invalid track_id: %s" % track_id, status=403)

    playlist.tracks.remove(track)
    db.session.commit()
    return Response('', status=200)


@app.route("/search", methods=['GET'])
def perform_search():
    """
    `GET` Search for a given query type and query string
    """
    q = request.args.get('q')
    q_type = request.args.get('q_type')
    resp = spotify_api_client().search_for(q, q_type)
    return Response(json.dumps(resp))
