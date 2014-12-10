# -*- coding: utf-8 -*-
import json
import music_app
import unittest

from player.models import *

class MusicAppTestCase(unittest.TestCase):
    
    """
    Test cases for endpoints provided by the music layer app
    """

    TESTING = True

    def create_app(self):
        return music_app.app

    def setUp(self):
        self.app = music_app.app.test_client()
        music_app.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        music_app.db.create_all()
        self.db = music_app.db

        self.user = User()
        self.db.session.add(self.user)
        self.db.session.commit()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()


    def test_playlist_creation(self):
        response = self.app.post('/playlists',
            data=json.dumps({'title': 'myplaylist'}),
            content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(data['title'], 'myplaylist')
        self.assertEqual(data['tracks'], [])
        self.assertEqual(data['user_id'], 1)



    def test_playlist_list(self):
        pl1 = Playlist('playlist_1', self.user)
        self.db.session.add(pl1)
        self.db.session.commit()

        response = self.app.get("/playlists")

        data = json.loads(response.data)
        playlist = data['playlists'][0]
        self.assertEqual(playlist['title'], 'playlist_1')
        self.assertEqual(playlist['tracks'], [])
        self.assertEqual(playlist['user']['id'], self.user.id)

    def test_playlist_read(self):
        pl = Playlist('playlist_2', self.user)
        self.db.session.add(pl)
        self.db.session.commit()

        response = self.app.get("/playlists/%s" % pl.id)

        data = json.loads(response.data)
        self.assertEqual(data['title'], 'playlist_2')
        self.assertEqual(data['tracks'], [])
        self.assertEqual(data['user_id'], 1)


    def test_playlist_update(self):
        pl = Playlist('my_playlist', self.user)
        self.db.session.add(pl)
        self.db.session.commit()

        response = self.app.put("/playlists/%s" % pl.id,
            data=json.dumps({'title': 'updated_playlist'}),
            content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(data['title'], 'updated_playlist')
        self.assertEqual(data['tracks'], [])
        self.assertEqual(data['user_id'], 1)   


    def test_playlist_delete(self):
        pl1 = Playlist('playlist1', self.user)
        self.db.session.add(pl1)
        self.db.session.commit()

        self.assertTrue(Playlist.query.get(pl1.id))

        response = self.app.delete("/playlists/%s" % pl1.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(None, Playlist.query.get(pl1.id))


    def test_playlist_add_track(self):
        trk = Track('0eGsygTp906u18L0Oimnem',
            'Mr. Brightside',
            'spotify:track:0eGsygTp906u18L0Oimnem')
        self.db.session.add(trk)

        pl1 = Playlist('playlist1', self.user)
        self.db.session.add(pl1)
        self.db.session.commit()

        pl1_id = pl1.id # cache playlist ID
        response = self.app.post("/playlists/%s/add_track" % pl1.id,
            data=json.dumps({'id': trk.id }),
            content_type='application/json')

        plx = Playlist.query.get(pl1_id)
        self.assertEqual('201 CREATED', response.status)
        self.assertEqual(1, len(plx.tracks))

        
    def test_playlist_delete_track(self):
        pl1 = Playlist('playlist1', self.user)
        self.db.session.add(pl1)
        self.db.session.commit()

        tk1 = Track('PeGsygTp906u18L0Oimnem',
            'Reasons Unknown',
            'spotify:track:0eGsygTp906u18L0Oimnem')
        self.db.session.add(tk1)
        self.db.session.commit()

        pl1.tracks.append(tk1)
        self.db.session.add(tk1)
        self.db.session.commit()

        pl1_id = pl1.id
        response = self.app.delete("/playlists/%s/remove_track" % pl1.id,
            data=json.dumps({'pk': tk1.id}),
            content_type='application/json')

        plx = Playlist.query.get(pl1_id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(plx.tracks))


    def test_search_uncached(self):
        response = self.app.get('/search?q=The%20Killers&q_type=album')
        self.assertEqual(200, response.status_code)


    def test_search_precached(self):
        """
        Tests the functionality of the pre-cache feature by making a query
        for an album that exists in the pre-cached data file
        """
        response = self.app.get('/search?q=We%20Are%20One&q_type=album')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('We Are One (Ole Ola) [The Official 2014 FIFA World Cup Song]', data[0]['name'])

if __name__ == '__main__':
    unittest.main()