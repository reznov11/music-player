**Link to web app running on heroku**: https://nameless-caverns-2924.herokuapp.com/

**Link to web app source repository**: https://github.com/tiabas/music-player

###Source Structure:
===================
```
.
├── Procfile

├── README 
	- This file

├── data
│   ├── player.sql
│   ├── player.sqlite3
│   ├── precached_album_data.json
│   ├── precached_artist_data.json
│   └── precached_track_data.json
	- player.sqlite3: preloaded sqilite database file for use with this application
	- precached_album_data.json: prefetched album data from Spotify's new-releases endpoint
	- precached_artist_data.json: empty file
	- precached_track_data.json: empty file
├── lib
│   
│   ├── oauth2
│   │   ├── __init__.py
│   │   └── client.py
	- Defines a simple OAuth2 client class for authorization through Spotify
	
│   ├── pre_cache.py
	- Defines three classes that perform fast lookup in a pre-cached Spotify dataset 

│   └── spotify
│       ├── __init__.py
│       └── client.py
	- Defines a simple client for performing searches using Spotify's web API

├── music_app.py
	- Initializes Flask web application

├── player
│   ├── __init__.py
│   ├── models.py
│   └── views.py
	- Models: Defines the models needed for creation of playlists i.e Track,
	  User, Playlist
	- Views: Defines the endpoints for creating, reading, updating and 
	  deleting playlists

├── requirements.txt
	- Specifies the libraries that this application depends on

├── shell.py
	- Launches and interactive python shell for interacting with the app

└── tests.py
	- Defines test cases for verifying behaviour of the classes defined in 
	  this application
```

###Libraries used:
===============
All the libraries below were used in order to save time and avoid duplicating 
functionality that was not necessarily relevant to the problem at hand

- requests: A python urllib wrapper with a cleaner interface
- Flask: A micro-framework for building web applications. Flask provides a barebones
         web utilities for a very basic python web apps
- marisa-trie: Provides a Trie datastrucure for fast lookup of items in pre-cached data cache
- SQLAlchemy: A python database wrapper the provides ORM functionalities
- virtualenv: Tool to create isolated Python environments
- Flask-Testing: Utilities for testing Flask based web applications
- Gunicorn: Python WSGI HTTP Server for UNIX

###Endpoints:
==========
```
help                           GET                          /
perform_search                 GET                          /search
get_or_create_playlists        POST,GET                     /playlists
view_or_update_playlist        PUT,GET,DELETE               /playlists/[playlist_id]
add_track_to_playlist          POST,OPTIONS                 /playlists/[playlist_id]/add_track
remove_track_to_playlist       DELETE                       /playlists/[playlist_id]/remove_track
```

###Running the app:
================
From the application root directory, inside a unix termianl, run:

- Installing dependencies
```bash
pip install -r requirements.txt
```

- Launching web app
```bash
python music_app.py
```

- Running tests:
```bash
python tests.py
```
