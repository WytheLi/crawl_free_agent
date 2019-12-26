#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 19-12-24 下午2:19
# @Description: 删除mongo中已失效代理，同时将有效代理缓存到redis中
# from spider_proxy_pool.common import request_test_proxy
import aiohttp
import asyncio
from spider_proxy_pool.clients import db, redis_conn

# 清空redis cache
redis_conn.delete("proxies")
# # 从mongo查询
# find_res = db["proxies"].find()
# for p in find_res:
#     print(p)
#     if not request_test_proxy(p):
#         db["proxies"].remove({"host": p["host"], "port": p["port"]})
#     else:   # 有效且支持https的代理
#         proxy = "http://"+p["host"]+":"+p["port"]
#         print("[OK]" + proxy)
#         redis_conn.sadd("proxies", proxy)


async def fetch_async(url, proxy):
    print(proxy)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, proxy=proxy, timeout=10) as resp:
                print("status:"+str(resp.status), proxy)
                redis_conn.sadd("proxies", proxy)
        except:
            print(proxy + " invalid proxy")
            db["proxies"].remove({"host": proxy[7:].split(":")[0], "port": proxy[7:].split(":")[1]})

find_res = db["proxies"].find()
tasks = [fetch_async("https://www.baidu.com", "http://"+p["host"]+":"+p["port"]) for p in find_res]
# tasks = [fetch_async("https://www.baidu.com", "http://47.103.117.209:3111") for p in find_res]


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(asyncio.gather(*tasks))
event_loop.close()
