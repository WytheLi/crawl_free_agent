#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 19-12-20 下午2:04
# @Description:
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spider_proxy_pool.spiders.get_proxies import GetProxiesSpider
from spider_proxy_pool.spiders.get_xici_proxies import GetXiciProxiesSpider

process = CrawlerProcess(get_project_settings())
# process.crawl(GetProxiesSpider)
process.crawl(GetXiciProxiesSpider)
process.start()

