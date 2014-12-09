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

class Client:

    SERVER_URL = 'https://api.spotify.com'

    def __init__(self, server_url=SERVER_URL, access_token=None, cache={}, pre_cache=None):
        self.server_url = server_url
        self.access_token = access_token
        self.cache = cache
        self.pre_cache = pre_cache

    def _make_request(self, url, params={}, headers={}):
        res = requests.get(url, params=params, headers=headers)
        if not res.ok:
            return None
        return res

    def _absolute_url(self, path):
        return "{0}{1}".format(self.server_url, path)

    def search_for(self, q, q_type):        
        cache_key = md5.new("{0}--{1}".format(q, q_type)).hexdigest()
        result = self.cache.get(cache_key, self.pre_cache.get(q, q_type))

        if result is None:
            search_url = self._absolute_url('/v1/search')
            result = self._make_request(search_url, { 'q': q, 'type': q_type })
            self.cache[cache_key] = result.content
        return json.loads(result.content)


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