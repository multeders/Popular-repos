import redis.asyncio as redis
import json
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_CACHE_EXPIRY = int(os.getenv("REDIS_CACHE_EXPIRY", 3600))  # 1 hour

redis_client = None

async def get_redis_connection():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    return redis_client

async def set_cache(key: str, value: dict, expiry: int = REDIS_CACHE_EXPIRY):
    redis = await get_redis_connection()
    if expiry is None:
        await redis.set(key, json.dumps(value))
    else:
        await redis.set(key, json.dumps(value), ex=expiry)

async def get_cache(key: str):
    redis = await get_redis_connection()
    cached_data = await redis.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None
