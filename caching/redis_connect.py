from typing import Any
import orjson
from redis import Redis

from settings import REDIS_CACHE_EXPIRES, REDIS_CONFIG


def get_redis() -> Redis:
    return Redis(**REDIS_CONFIG)


class Cache():
    def __init__(self, redis: Redis | None = None) -> None:
        if redis:
            self._redis = redis
        else:
            self._redis = Redis(**REDIS_CONFIG)

    def cache_page(self, url: str, content: Any, page: int = 1):
        if isinstance(content, dict):
            content = orjson.dumps(content)
        elif isinstance(content, str):
            content = content.encode()
        self._redis.setex(name=f"{url}{page}",
                          time=REDIS_CACHE_EXPIRES,
                          value=content)
        last_page_key = f"last:{url}"
        last_cached = self._redis.get(last_page_key)
        if last_cached == None or int(last_cached) < page:
            self._redis.setex(name=last_page_key,
                              time=REDIS_CACHE_EXPIRES,
                              value=page)

    def get_page(self, url: str, page: int = 1) -> bytes | None:
        return self._redis.get(name=f"{url}{page}")

    def flush_cache(self, url: str):
        last_cached = self._redis.get(f"last:{url}")
        if last_cached:
            if isinstance(last_cached, bytes):
                last_cached = last_cached.decode()
            self._redis.delete(f"{url}{last_cached}")
