#!/usr/bin/env python3
"""Module: LRUCache """
BaseCaching = __import__("base_caching").BaseCaching


class LRUCache (BaseCaching):
    """A LRU cache implementation"""

    def __init__(self):
        """Creates a cache instance
        """
        super().__init__()
        self.cache_keys = {}
        self.count = 0

    def put(self, key, item):
        """Add an item in the cache
        """
        if key is None or item is None:
            return

        size = len(self.cache_data)
        key_exists = key in self.cache_data

        if size >= BaseCaching.MAX_ITEMS and not key_exists:
            discard_key = self._get_least_key()
            self.cache_keys.pop(discard_key)
            self.cache_data.pop(discard_key)
            print("DISCARD: {}".format(discard_key))

        self.cache_data[key] = item
        self._usage(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None:
            return None

        data = self.cache_data.get(key, None)
        if data is not None:
            self._usage(key)
        return data

    def _get_least_key(self):
        """ Get least recent used key
        """
        items = list(self.cache_keys.values())
        least = items[0]
        for item in items:
            if item['usage'] < least['usage']:
                least = item
        return least['key']

    def _usage(self, key):
        """ Tracks usage of cache data
        """
        self.cache_keys[key] = {'key': key, 'usage': self.count}
        self.count += 1
