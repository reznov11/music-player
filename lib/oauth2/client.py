# -*- coding: utf-8 -*-
import urllib, urllib2
import json, base64

class OAuth2Client:

    """
    Simplifies the process of obtaining OAuth2 access tokens
    """
    def __init__(self, client_id, client_secret, server='https://accounts.spotify.com', authorize_path='/authorze', tokens_path='/api/token'):
        self.server_url = server
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorize_path = authorize_path
        self.tokens_path = tokens_path

    def authorize_url(self, redirect_uri, response_type, state='', scope='', show_dialog='true'):
        query_string = urllib.urlencode({
            'client_id': self.client_id,
            'redirect_uri': redirect_uri ,
            'state': state,
            'response_type': response_type,
            'scope': scope,
            'show_dialog': show_dialog
        })
        return "{0}/authorize?{1}".format(self.server_url, query_string)

    def get_tokens(self, code, redirect_uri, grant_type='authorization_code'):
        url = "{0}/{1}".format(self.server_url, self.tokens_path)
        data = urllib.urlencode({
            'code': code,
            'grant_type': grant_type,
            'redirect_uri': redirect_uri
        })
        headers = { 'Authorization' : "Basic %s" % base64.standard_b64encode("{0}:{1}".format(self.client_id, self.client_secret))}
        request = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(request)
        return response.read()
