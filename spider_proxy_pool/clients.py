#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 19-12-20 下午2:23
# @Description:
import redis
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings

# 获取settings中的配置信息
# settings = get_project_settings()
# for key, value in settings.items():
#     print(key, value)
settings = get_project_settings()

mongo_conn = MongoClient(
    host=settings["MONGO_HOST"],
    port=settings["MONGO_PORT"],
    username=settings["MONGO_USERNAME"],
    password=settings["MONGO_PASSWORD"]
)
db = mongo_conn[settings["MONGO_DB"]]

mongo_conn_1 = MongoClient(
    host=settings["MONGO_HOST_1"],
    port=settings["MONGO_PORT_1"],
    username=settings["MONGO_USERNAME_1"],
    password=settings["MONGO_PASSWORD_1"]
)
db_1 = mongo_conn_1[settings["MONGO_DB_1"]]

# 创建redis连接池
redis_conn_pool = redis.ConnectionPool(
    host=settings["REDIS_HOST"],
    port=settings["REDIS_PORT"],
    db=settings["REDIS_DB"],
    password=settings["REDIS_PASSWORD"]
)
# 创建连接对象
redis_conn = redis.Redis(connection_pool=redis_conn_pool)

# 线下
redis_conn_pool_1 = redis.ConnectionPool(
    host=settings["REDIS_HOST_LOCALHOST"],
    port=settings["REDIS_PORT"],
    db=settings["REDIS_DB"],
    password=settings["REDIS_PASSWORD"]
)
redis_conn_1 = redis.Redis(connection_pool=redis_conn_pool_1)


if __name__ == '__main__':
    # 本地mongo备份到线上
    # res = db['proxies'].find()
    # print(res)
    # for sing in res:
    #     data = {
    #         'host': sing['host'],
    #         'port': sing['port'],
    #         'location': sing['location'],
    #         'operators': sing['operators'],
    #         'is_support_https': sing['is_support_https'],
    #         'is_support_post': sing['is_support_post'],
    #         'type': sing['type'],
    #         'delay': sing['delay'],
    #         'relative_time': sing['relative_time'],
    #         'create_time': sing['create_time'],
    #     }
    #     res_id = db_1['proxies'].insert_one(data)
    #     print(res_id)
    proxies = redis_conn_1.smembers("proxies")
    for p in proxies:
        print(p)
        redis_conn.sadd("proxies", p)
