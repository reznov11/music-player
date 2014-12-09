App Link: http://music-player.herokuapp.com/
App Repo: https://github.com/tiabas/music-player

How is source code organized:

.
├── Procfile

├── README 
	- This file

├── data
│   ├── player.sqlite3
│   └── precache_data.json
	- player.sqlite3: preloaded sqilite database file for use with this application
	- precache_data.json: prefetched album data from Spotify's new-releases endpoint

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
	- Models: Defines the models needed for creation of playlists i.e Track, User, Playlist
	- Views: Defines the endpoints for creating, reading, updating and deleting playlists

├── requirements.txt
	- Specifies the libraries that this application depends on

├── shell.py
	- 

└── tests.py
	- Defines test cases for verifying behaviour of the classes defined in this application


Libraries used:
- requests: A python urllib wrapper with a cleaner interface
- Flask:
- marisa-trie:
