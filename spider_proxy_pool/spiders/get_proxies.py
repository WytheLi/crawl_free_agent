# -*- coding: utf-8 -*-
import scrapy

from spider_proxy_pool.items import SpiderProxyPoolItem


class GetProxiesSpider(scrapy.Spider):
    name = 'get_proxies'
    allowed_domains = ['ip.ihuan.me']
    start_urls = ['https://ip.ihuan.me/']
    custom_settings = {
        "ITEM_PIPELINES": {'spider_proxy_pool.pipelines.SpiderProxyPoolPipeline': 300},
        # "DOWNLOADER_MIDDLEWARES": {'spider_proxy_pool.middlewares.ProxyDownloaderMiddleware': 600},
        'DEFAULT_REQUEST_HEADERS': {'Referer': 'https://ip.ihuan.me/'}
        # # 设置log日志
        # 'LOG_LEVEL': 'ERROR',
        # 'LOG_FILE': './logs/spider.log'
    }
    _page = 1

    def make_requests_from_url(self, url):
        # self.logger.debug('Try first time')
        print('Try first time')
        return scrapy.Request(url=url, meta={'download_timeout': 10}, callback=self.parse, dont_filter=False)

    def parse(self, response):
        """
        主页解析
        :param response:
        :return:
        """
        print(response.url)
        # 提取数据
        # tr_list = response.xpath('//div[@class="greyframe"]/table[2]/tr//tr')
        tr_list = response.xpath('//div[@class="table-responsive"]//tr')
        for tr in tr_list:
            item = SpiderProxyPoolItem()
            item["host"] = tr.xpath('./td[1]//text()').extract_first() if tr.xpath(
                './td[1]//text()').extract_first() else ""
            item["port"] = tr.xpath('./td[2]//text()').extract_first() if tr.xpath(
                './td[2]//text()').extract_first() else ""
            item["location"] = tr.xpath('./td[3]//text()').extract() if tr.xpath('./td[3]//text()').extract() else []
            item["operators"] = tr.xpath('./td[4]//text()').extract_first() if tr.xpath(
                './td[4]//text()').extract_first() else ""
            item["is_support_https"] = tr.xpath('./td[5]//text()').extract_first() if tr.xpath(
                './td[5]//text()').extract_first() else ""
            item["is_support_post"] = tr.xpath('./td[6]//text()').extract_first() if tr.xpath(
                './td[6]//text()').extract_first() else ""
            item["type"] = tr.xpath('./td[7]//text()').extract_first() if tr.xpath(
                './td[7]//text()').extract_first() else ""
            item["delay"] = tr.xpath('./td[8]//text()').extract_first() if tr.xpath(
                './td[8]//text()').extract_first() else ""
            item["relative_time"] = tr.xpath('./td[9]//text()').extract_first() if tr.xpath(
                './td[9]//text()').extract_first() else ""
            yield item
            # yield返回详情页请求对象
            # yield scrapy.Request(item["detail_url"], callback=self.detail_parse, meta={"item": item})
        # 处理分页
        # next_url = response.xpath('//a[text()="»"]/@href').extract_first()
        next_url = response.xpath('//a[@aria-label="Next"]/@href').extract_first()
        if next_url:
            if self._page < 20:
                next_url = "https://ip.ihuan.me/" + next_url
                self._page += 1
                yield scrapy.Request(next_url, callback=self.parse, dont_filter=False)

    # def detail_parse(self, response):
    #     """
    #     详情页解析
    #     :return:
    #     """
    #     pass
