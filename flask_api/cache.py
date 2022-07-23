import redis
import os
from dotenv import load_dotenv
load_dotenv()


class Cache:
    base: int = 0

    def __init__(self):
        url = f"{os.environ.get('REDIS_HOST')}/{Cache.base}"
        Cache.base += 1
        self.cache = redis.from_url(url, max_connections=20, decode_responses=True)

    def get(self, key, **kwargs):
        return self.cache.get(key, **kwargs)

    def set(self, key, value, **kwargs):
        return self.cache.set(key, value, **kwargs)

    def get_cache(self):
        return self.cache
