#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 19-12-25 下午6:36
# @Description: 博客参考： https://www.cnblogs.com/ssyfj/p/9222342.html
import aiohttp
import asyncio

from spider_proxy_pool.clients import db


async def fetch_async(url, proxy):
    print(proxy)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, proxy=proxy, timeout=10) as resp:
                print("status:"+str(resp.status), proxy)
        except:
            print(proxy + " invalid proxy")
            db["proxies"].remove({"host": proxy[7:].split(":")[0], "port": proxy[7:].split(":")[1]})

find_res = db["proxies"].find()
tasks = [fetch_async("https://www.baidu.com", "http://"+p["host"]+":"+p["port"]) for p in find_res]
# tasks = [fetch_async("https://www.baidu.com", "http://47.103.117.209:3111") for p in find_res]


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(asyncio.gather(*tasks))
event_loop.close()
