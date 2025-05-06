import redis
from api.config import LocalConfig, ComposeConfig


def redis_connection():
    return redis.Redis(
        # host=LocalConfig.HOST,
        # port=LocalConfig.PORT,
        host=ComposeConfig.HOST,
        port=ComposeConfig.PORT,
        decode_responses=True,
    )
