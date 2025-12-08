import json
from functools import wraps
from aiocache import Cache
from fastapi import HTTPException
from pydantic_settings import BaseSettings


class RedisSetting(BaseSettings):
    port: int = 6379
    host: str = "localhost"

    class Config:
        env_prefix = "REDIS_"


redis_settings = RedisSetting()


def cache_response(ttl: int = 60, namespace: str = "main"):
    """
    Caching decorator for FastAPI endpoints.

    ttl: Time to live for the cache in seconds.
    namespace: Namespace for cache keys in Redis.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            input_key = [str(arg) for arg in args]
            cache_key = f"{namespace}:{input_key}"

            cache = Cache.REDIS(
                endpoint=redis_settings.host,
                port=redis_settings.port,
                namespace=namespace,
            )

            # Try to retrieve data from cache
            cached_value = await cache.get(cache_key)
            if cached_value:
                return json.loads(cached_value)  # Return cached data

            # Call the actual function if cache is not hit
            response = await func(*args, **kwargs)

            try:
                # Store the response in Redis with a TTL
                await cache.set(cache_key, json.dumps(response), ttl=ttl)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error caching data: {e}")

            return response

        return wrapper

    return decorator
