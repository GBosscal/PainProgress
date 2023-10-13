"""
@Project: BackendForPain
@File: redis_helper.py
@Auth: Bosscal
@Date: 2023/10/7
@Description: 
"""
import redis

from config import Config

# 创建一个Redis连接对象
redis_client = redis.StrictRedis(
    host=Config.RedisHost, port=Config.RedisPort,
    db=Config.RedisDataBase, password=Config.RedisPSWD
)


def set_redis_data(key: str, value: str, expire: int = 0):
    if expire == 0:
        redis_client.set(key, value)
    else:
        redis_client.setex(key, expire, value)


def get_redis_data_by_key(key: str):
    return redis_client.get(key).decode("utf-8")


def set_redis_data_by_hash(list_name: str, key: str, data: str):
    redis_client.hset(list_name, key, data)


def get_redis_data_by_hash(list_name: str, key: str):
    data = redis_client.hget(list_name, key)
    return data
