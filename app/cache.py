import os

from redis import Redis
from redis.exceptions import RedisError

_client = None


def _get_client():
    global _client
    if _client is None:
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        _client = Redis.from_url(redis_url, decode_responses=True)
    return _client


def cache_get(key: str) -> str | None:
    try:
        return _get_client().get(key)
    except RedisError:
        return None


def cache_set(key: str, value: str, ttl_seconds: int = 3600) -> None:
    try:
        _get_client().setex(key, ttl_seconds, value)
    except RedisError:
        return
