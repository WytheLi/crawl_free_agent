# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import telnetlib
import time

import requests

from spider_proxy_pool.clients import db


class SpiderProxyPoolPipeline(object):
    def process_item(self, item, spider):
        # print(item)
        spider.logger.info(item)
        if item["host"] and item["port"]:
            proxy = db["proxies"].find_one({"host": item["host"], "port": item["port"]})
            if not proxy:
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item["create_time"] = now_time
                db["proxies"].insert_one(item)

    def telnet_test_ip(self, host, port):
        """
        telnet测试过关，不一定可用
        保险起见，请求测试
        :param ip:
        :param port:
        :return:
        """
        try:
            telnetlib.Telnet(host, port, timeout=2)
            print("["+host+":"+port+"]代理ip有效！")
            return True
        except:
            print("代理ip无效！")
            return False


class SpiderXiciProxyPoolPipeline(object):
    def process_item(self, item, spider):
        # print(item)
        spider.logger.info(item)
        if item["host"] and item["port"]:
            proxy = db["proxies"].find_one({"host": item["host"], "port": item["port"]})
            if not proxy:
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item["create_time"] = now_time
                db["proxies"].insert_one(item)

