#!/usr/bin/env python3
"""Module: LIFOCache """
BaseCaching = __import__("base_caching").BaseCaching


class LIFOCache (BaseCaching):
    """A FIFO cache implementation"""

    def __init__(self):
        """Creates a cache instance
        """
        super().__init__()
        self.cache_keys = []

    def put(self, key, item):
        """Add an item in the cache
        """
        if key is None or item is None:
            return

        size = len(self.cache_data)
        key_exists = key in self.cache_data

        if size >= BaseCaching.MAX_ITEMS and not key_exists:
            discard_key = self.cache_keys.pop()
            self.cache_data.pop(discard_key)
            print("DISCARD: {}".format(discard_key))

        if key_exists:
            self.cache_keys.remove(key)
        self.cache_data[key] = item
        self.cache_keys.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None:
            return None
        return self.cache_data.get(key, None)
