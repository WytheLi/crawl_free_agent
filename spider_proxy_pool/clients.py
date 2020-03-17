#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 19-12-20 下午2:23
# @Description:
import random

import pymysql
import redis
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from spider_proxy_pool import constants


class Mongo(object):
    mongo_conn = None

    def __init__(self,
                 mongo_host="localhost",
                 mongo_port=27017,
                 mongo_user="root",
                 mongo_password="",
                 mongo_db=""):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password
        self.mongo_db = mongo_db

        if not self.mongo_conn:
            self.mongo_conn = MongoClient(
                host=self.mongo_host,
                port=self.mongo_port,
                username=self.mongo_user,
                password=self.mongo_password
            )

    def get_mongo_conn(self):
        return self.mongo_conn

    def get_db(self):
        return self.mongo_conn[self.mongo_db]

    def __del__(self):
        self.mongo_conn.close()


mongo = Mongo(mongo_host=constants.MONGO_HOST,
              mongo_port=constants.MONGO_PORT,
              mongo_user=constants.MONGO_USERNAME,
              mongo_password=constants.MONGO_PASSWORD,
              mongo_db=constants.MONGO_DB)
mongo_conn = mongo.get_mongo_conn()
db = mongo.get_db()
# mongo_conn = MongoClient(
#     host=constants.MONGO_HOST,
#     port=constants.MONGO_PORT,
#     username=constants.MONGO_USERNAME,
#     password=constants.MONGO_PASSWORD
# )
# # client = MongoClient(host=config.HOST, port=config.PORT, username=config.USERNAME, password=config.PASSWORD, retryWrites=False)
# db = mongo_conn[constants.MONGO_DB]

# mysql_conn = pymysql.connect(
#     host=constants.MYSQL_HOST,
#     user=constants.MYSQL_USERNAME,
#     password=constants.MYSQL_PASSWORD,
#     db=constants.MYSQL_DB,
#     # cursorclass=pymysql.cursors.DictCursor,  # 修改返回的数据类型为字典
#     charset='utf8mb4'
# )

# 创建redis连接池
redis_conn_pool = redis.ConnectionPool(
    host=constants.REDIS_HOST,
    port=constants.REDIS_PORT,
    db=constants.REDIS_DB,
    password=constants.REDIS_PASSWORD
)
# 创建连接对象
redis_conn = redis.Redis(connection_pool=redis_conn_pool)


# 创建本地redis连接池
redis_conn_pool_l = redis.ConnectionPool(
    host=constants.REDIS_HOST_L,
    port=constants.REDIS_PORT_L,
    db=constants.REDIS_DB_L,
    password=constants.REDIS_PASSWORD_L
)
# 创建连接对象
redis_conn_l = redis.Redis(connection_pool=redis_conn_pool_l)

if __name__ == "__main__":
    _proxies = redis_conn.smembers("proxies")
    proxy = random.choice(list(_proxies)).decode() if _proxies else ""
    print(proxy)