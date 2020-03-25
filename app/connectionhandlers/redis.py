import logging
import os

import aioredis

logger = logging.getLogger(__name__)


def get_redis() -> aioredis.Redis:
    global redis
    return redis


def connect():
    global redis
    redis = await aioredis.create_redis_pool(os.getenv('redishost', 'redis://redis:6379'))
    redis.exists()


def disconnect():
    global redis
    redis.close()
    await redis.wait_closed()
