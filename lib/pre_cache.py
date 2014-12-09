import json, marisa_trie

class AlbumPreCache:

	def __init__(self, source_file='precache_data.json'):
		self._cached_data = {}
		self.source_file = source_file
		self._warm = False

	def get(self, key):
		if not self._warm:
			self._warm_cache()
		items = self._trie.items(unicode(key).lower())
		return [self._cached_data.get(unicode(i[1])) for i in items]

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




