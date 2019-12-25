# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderProxyPoolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    host = scrapy.Field()
    port = scrapy.Field()
    location = scrapy.Field()
    operators = scrapy.Field()
    is_support_https = scrapy.Field()
    is_support_post = scrapy.Field()
    type = scrapy.Field()
    delay = scrapy.Field()
    relative_time = scrapy.Field()

    _id = scrapy.Field()
    create_time = scrapy.Field()    # 数据存储时间
