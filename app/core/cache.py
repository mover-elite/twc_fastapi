import redis

redis_cache = redis.Redis(decode_responses=True)
