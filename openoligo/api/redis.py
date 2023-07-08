"""
Connection to Redis database
"""
import os

import redis

host: str = os.environ.get("OO_REDIS_HOST", "localhost")
port: int = int(os.environ.get("OO_REDIS_PORT", 42445))
password: str = os.environ.get("OO_REDIS_PASSWORD", "")

red = redis.Redis(
    host=host,
    port=port,
    password=password,
    ssl=True,
)


def get_redis() -> redis.Redis:
    """Get Redis connection"""
    return red
