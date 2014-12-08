import json
import music_app
import unittest

from player.models import *

class MusicAppTestCase(unittest.TestCase):
    
    # SQLALCHEMY_DATABASE_URI = "sqlite://"
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
        self.assertEqual('200 OK', response.status)
        self.assertEqual(None, Playlist.query.get(pl1.id))


    def test_playlist_add_track(self):
        pl1 = Playlist('playlist1', self.user)
        self.db.session.add(pl1)
        self.db.session.commit()

        response = self.app.post("/playlists/%s/add_track" % pl1.id,
            data=json.dumps({
                'title': '0eGsygTp906u18L0Oimnem',
                'track_id': 'Mr. Brightside',
                'uri': 'spotify:track:0eGsygTp906u18L0Oimnem'
            }),
            content_type='application/json')
        plx = Playlist.query.get(pl1.id)
        self.assertEqual('204 NO CONTENT', response.status)
        self.assertEqual(0, len(plx.tracks))
        
if __name__ == '__main__':
    unittest.main()