import redis.asyncio as redis

redis_pool = redis.ConnectionPool.from_url(
    "redis://redis:6379/0", max_connections=10, decode_responses=True
)
