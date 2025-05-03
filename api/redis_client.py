import redis
from api.config import RedisConfig


def redis_connection():
    return redis.Redis(
        host=RedisConfig.HOST,
        port=RedisConfig.PORT,
        decode_responses=True,
    )
