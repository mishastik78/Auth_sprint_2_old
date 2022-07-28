import os

import dotenv
import redis

dotenv.load_dotenv()


class Cache:
    base: int = 0

    def __init__(self):
        url = f"{os.environ.get('REDIS_URL')}/{Cache.base}"
        Cache.base += 1
        self.cache = redis.from_url(url, max_connections=20, decode_responses=True)

    def get(self, key, **kwargs):
        return self.cache.get(key, **kwargs)

    def set(self, key, value, **kwargs):
        return self.cache.set(key, value, **kwargs)

    def get_cache(self):
        return self.cache
