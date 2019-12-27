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


# 创建redis连接池
redis_conn_pool = redis.ConnectionPool(
    host=settings["REDIS_HOST"],
    port=settings["REDIS_PORT"],
    db=settings["REDIS_DB"],
    password=settings["REDIS_PASSWORD"]
)
# 创建连接对象
redis_conn = redis.Redis(connection_pool=redis_conn_pool)
