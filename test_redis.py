#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 19-12-25 下午2:20
# @Description:
import random

from spider_proxy_pool.clients import redis_conn

# redis-server v3.0.6 v4.0.9亲测
# 有序集合
# res_zadd = redis_conn.zadd("proxies", {
#     "http://163.172.148.62:8811": 1,
#     "http://222.94.125.152:1080": 2,
#     "http://51.158.119.88:8811": 3,
#     "http://153.101.64.50:12034": 4,
#     "http://118.89.234.236:8787": 5,
#     "http://41.198.58.66:80": 6,
#     "http://51.158.113.142:8811": 7,
#     "http://51.158.108.135:8811": 8,
#     "http://128.199.241.212:8080": 9,
#     "http://51.91.212.159:3128": 10,
# })
# print(res_zadd)
# redis_conn.zrem("proxies", "bbb", "ccc")
#
# res_zrange = redis_conn.zrange("proxies", 0, -1)
# print(res_zrange)

# 无序集合
res_sadd = redis_conn.sadd("set_test", "aaa", "bbb")
print(res_sadd)
# redis_conn.srem("set_test", "aaa")
res_smembers = redis_conn.smembers("set_test")
print(res_smembers, type(res_smembers))

# 列表
# res_lpush = redis_conn.lpush("list_test", "aaa", "bbb")
# print(res_lpush)
# res_lrange = redis_conn.lrange("list_test", 0, -1)
# print(res_lrange)
