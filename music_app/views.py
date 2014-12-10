from flask import request, Response, jsonify, Blueprint

from lib.spotify.client import Client as spotify_api_client

from music_app import db, app

from . models import *

# mod = Blueprint('player', __name__, url_prefix='')


@app.route("/playlists", methods=['GET', 'POST'])
def get_or_create_playlists():
    """
    Create a playlist or, returns a list of playlists 
    belonging to the current user.

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
        return jsonify(playlists)


@app.route("/playlists/<playlist_id>", methods=['GET', 'PUT', 'DELETE'])
def view_or_update_playlist(playlist_id):
    """
    Fetches a playlist with the provides playlist primary key.
    If the playlist is not found, a 404 response is returned. 
    If the playlist title Updates the title for an existing playlist 
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
            tracks=pl.tracks)


@app.route("/playlists/<playlist_id>/add_track", methods=['POST'])
def add_track_to_playlist(playlist_id):
    # add track to playlist
    pl = Playlist.query.filter_by(id=playlist_id, user_id=1).first_or_404()
    data = request.get_json()
    track_id = data['track_id']

    # fetch track data??
    track = Track.query.filter_by(track_id=track_id).first()

    # if track with ID is does not exist in DB, attempt to fetch it from
    # spotify and then create it
    if track is None:
        track_data = spotify_api_client().get_track(track_id)

        if track_data is None:
            return Response("invalid track_id: %s" % track_id, status=403)
        parsed = json.loads(track_data.content)
        track = Track(
            track_id=parsed['id'],
            uri=parsed['uri'],
            title=parsed['name'])
        db.session.add(track)
        db.session.commit()

        pl.tracks.append(track)
        db.session.commit()
        return Response('', status=201)
    return Response('', status=204)

@app.route("/playlists/<playlist_id>/remove_track", methods=['DELETE'])
def remove_track_to_playlist(playlist_id):
    # remove track from playlist
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
    q = request.args.get('q')
    q_type = request.args.get('q_type')
    resp = spotify_api_client().search_for(q, q_type)
    return Response(json.dumps(resp))