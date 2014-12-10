import requests, md5, json

import logging
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig() 
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

from .. import pre_cache

from music_app import app

class Client:

    """
    This is a simple client class to handle the retrieval of data
    using spotifies Web API.

    For HTTP requests, this class relies on the `requests` library
    which has a  more user friendly API than python's urllib

    The client has references to three pre cache objects that are used
    for fast lookup of user submitted queries. The pre-cache objects 
    contain pre-loaded album, artist and track data from Spotify based 
    on popularity. For the purposes of this code test, we are relying 
    on data from the new-releases under the assumption that a user is more
    likely to search for new tracks, albums and artists

    This class also maintais references to the most recent searches that
    have been made through the application. For the purposes of this code 
    test, the recent search are stored in an in-memory Hash data structure.

    When a search query is made, the client will first attempt to retrieve 
    data from the recent searches cache based on the query type and query key.
    If there is no matching entry in this cache, a lookup is done in the 
    appropriate pre_cache object. If a match is found in the pre-cache, the 
    values are returned. If the is not hit in any of the caches, the data is 
    retrieved through Spotify's search API. The data is stored in the recent 
    searches cache and returned
    """

    SERVER_URL = 'https://api.spotify.com'

    def __init__(self, server_url=SERVER_URL, access_token=None, cache={}):
        self.server_url = server_url
        self.access_token = access_token
        self.cache = cache
        self.album_pre_cache = pre_cache.AlbumPreCache(app.config['PRECACHED_ALBUM_DATA'])
        self.artist_pre_cache = pre_cache.ArtistPreCache(app.config['PRECACHED_ARTIST_DATA'])
        self.track_pre_cache = pre_cache.TrackPreCache(app.config['PRECACHED_TRACK_DATA'])

    def _make_request(self, url, params={}, headers={}):
        res = requests.get(url, params=params, headers=headers)
        if not res.ok:
            return None
        return res

    def _absolute_url(self, path):
        return "{0}{1}".format(self.server_url, path)


    def search_for(self, q, q_type):
        """
        Create a cache key based on the input parameters and attempt
        to fetch query from cache.
        """
        cache_key = md5.new("{0}--{1}".format(q, q_type)).hexdigest()
        data = self.cache.get(cache_key, [])

        if not data:
            if q_type == 'artist':
                pre_cache = self.artist_pre_cache
            elif q_type == 'album':
                pre_cache = self.album_pre_cache
            elif q_type == 'track':
                pre_cache = self.track_pre_cache
            else:
                raise Exception('Invalid query type')
            data = pre_cache.get(q)

        if not data:
            search_url = self._absolute_url('/v1/search')
            response = self._make_request(search_url, { 'q': q, 'type': q_type })
            if response.status_code != 200:
                return None
            data = response.json()
            self.cache[cache_key] = data
        return data


    def search_albums(self, query):
        return self._search_for(query, 'album')

    def search_artists(self, query):
        return self._search_for(query, 'artist')

    def search_tracks(self, query):
        return self._search_for(query, 'track')

    def get_track(self, track_id):
        return self._make_request(self._absolute_url("/v1/tracks/%s" % track_id))

    def get_new_releases(self, country=None, headers=None):
        return self._make_request(self._absolute_url("/v1/browse/new-releases"))

    def get_album_tracks(self, album_id):
        return self._make_request(self._absolute_url("/v1/albums/%s/tracks" % album_id))