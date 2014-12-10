import json, marisa_trie

class PreCache:
	"""
	Acts as a cache for key/value pairs. Uses a Trie data structure
	to allow for the retrival of multiple values whose keys contain
	a specified prefix.
	"""

	def __init__(self, source_file):
		self._cached_data = {}
		self.source_file = source_file
		self._warm = False

	def get(self, key):
		if not self._warm:
			self._warm_cache()
		items = self._trie.items(unicode(key).lower())

		return [self._cached_data.get(unicode(i[1])) for i in items]

	def _warm_cache(self):
		raise NotImplementedError()


class AlbumPreCache(PreCache):
	"""
	Precaches a list of Spotify album objects using the album name
	as a key and the album json data as the value.

	NOTE: The source file name is harcoded due to time constraints. Ideally
	this would be injected at the time of instantiation of the class
	"""

	def _warm_cache(self):
		if self._warm:
			return

		with open(self.source_file, 'r') as f:
			data = f.read()

		albums_list = json.loads(data)
		keys = [unicode(album['name']).lower() for album in albums_list]
		self._trie = marisa_trie.Trie(keys)

		for album in albums_list:
			name = album.get('name', False)
			cache_key = self._trie.key_id(unicode(name).lower())
			self._cached_data[unicode(cache_key)] = album
		self._warm = True


class ArtistPreCache(PreCache):
	"""
	Precaches a list of Spotify artist objects using the artist name
	as a key and the album json data as the value

	NOTE: This has not been implemented in the interest of time
	"""

class TrackPreCache(PreCache):
	"""
	Precaches a list of Spotify artist objects using the track name
	as a key and the album json data as the value

	NOTE: This has not been implemented in the interest of time
	"""
