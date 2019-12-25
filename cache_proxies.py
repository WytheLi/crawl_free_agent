#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 19-12-24 下午2:19
# @Description: 删除mongo中已失效代理，同时将有效代理缓存到redis中
from spider_proxy_pool.common import request_test_proxy
from spider_proxy_pool.clients import db, redis_conn

# 清空redis cache
redis_conn.delete("proxies")
# 从mongo查询
find_res = db["proxies"].find()
for p in find_res:
    print(p)
    if not request_test_proxy(p):
        db["proxies"].remove({"host": p["host"], "port": p["port"]})
    else:   # 有效且支持https的代理
        proxy = "http://"+p["host"]+":"+p["port"]
        print("[OK]" + proxy)
        redis_conn.sadd("proxies", proxy)
