# -*- coding: utf-8 -*-
import scrapy

from spider_proxy_pool.items import SpiderProxyPoolItem


class GetXiciProxiesSpider(scrapy.Spider):
    name = 'get_xici_proxies'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn']
    custom_settings = {
        "ITEM_PIPELINES": {'spider_proxy_pool.pipelines.SpiderXiciProxyPoolPipeline': 301},
        # "DOWNLOADER_MIDDLEWARES": {'spider_proxy_pool.middlewares.ProxyDownloaderMiddleware': 600},
        # # 设置log日志
        # 'LOG_LEVEL': 'ERROR',
        # 'LOG_FILE': './logs/spider.log'
    }

    def parse(self, response):
        """
        主页解析
        :param response:
        :return:
        """
        print(response.url)
        # 提取数据
        # tr_list = response.xpath('//div[@class="greyframe"]/table[2]/tr//tr')
        tr_list = response.xpath('//table[@id="ip_list"]//tr')
        for tr in tr_list[1:]:
            item = SpiderProxyPoolItem()
            item["host"] = tr.xpath('./td[2]//text()').extract_first() if tr.xpath(
                './td[2]//text()').extract_first() else ""
            item["port"] = tr.xpath('./td[3]//text()').extract_first() if tr.xpath(
                './td[3]//text()').extract_first() else ""
            item["location"] = tr.xpath('./td[4]//text()').extract() if tr.xpath('./td[4]//text()').extract() else []
            item["operators"] = ""
            item["is_support_https"] = 1 if tr.xpath(
                './td[6]//text()').extract_first() == "HTTPS" else 0
            item["is_support_post"] = ""
            item["type"] = ""
            item["delay"] = ""
            item["relative_time"] = tr.xpath('./td[9]//text()').extract_first() if tr.xpath(
                './td[9]//text()').extract_first() else ""
            yield item
            # yield返回详情页请求对象
            # yield scrapy.Request(item["detail_url"], callback=self.detail_parse, meta={"item": item})
        # 处理分页
        next_url = response.xpath('//a[text()="下一页 ›"]/@href').extract_first()
        next_url = 'https://www.xicidaili.com' + next_url
        yield scrapy.Request(next_url, callback=self.parse, dont_filter=False)
