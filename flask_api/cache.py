from abc import ABC, abstractmethod
from typing import Any, Awaitable, Coroutine

import redis
from flask_api import app


class Cache:
    base: int = 0

    def __init__(self):
        url = app.config['REDIS_URL'] + f'/{Cache.base}'
        Cache.base += 1
        self.cache = redis.from_url(url, max_connections=20, decode_responses=True)

    def get(self, key, **kwargs):
        return self.cache.get(key, **kwargs)

    def set(self, key, value, **kwargs):
        return self.cache.set(key, value, **kwargs)

    def get_cache(self):
        return self.cache
