#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 19-12-20 下午2:23
# @Description:
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
    # 字符串操作
    # redis_conn.set("start_time", "2019-10-10")
    # res1 = redis_conn.get("start_time").decode()
    # print(res1)
    # redis_conn.setex("骑士"+"time_node_aaa", 300, "aaaa")
    # print(redis_conn.get("骑士" + "time_node_aaa"))

    # res = redis_conn.smembers("proxies")
    # print(res)

    # 列表操作
    # redis_conn.lpush("login_user_list", "aaa")
    # redis_conn.lpush("login_user_list", "bbb")
    # list_len = redis_conn.llen("login_user_list")
    # print(list_len)
    # res_list = redis_conn.lrange("login_user_list", 0, list_len-1)
    # print(res_list)
    # res = db["mn_sports_qq_nba_text"].delete_many({"$and": [{"create_time": {"$gte": '2020-01-08'}}, {"create_time": {"$lte": '2020-01-09'}}]})
    # print(res.deleted_count)

    # res = redis_conn.srandmember("proxies")
    # print(res)

    redis_conn.set("aaa", 1)
    res = redis_conn.get("aaa")
    print(res)
