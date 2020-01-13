# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import hashlib
import random
import time

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from w3lib.url import safe_url_string
from six.moves.urllib.parse import urljoin

from spider_proxy_pool.clients import redis_conn
from spider_proxy_pool.common import request_test_proxy, ChromeDriver
from spider_proxy_pool.clients import db
from lxml import etree


class SpiderProxyPoolSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpiderProxyPoolDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyDownloaderMiddleware(object):
    def __init__(self):
        self.orderno = "ZF20191298120NifqXV"
        self.secret = "65a61c2fe56840488037cc507b6620f4"
        # 将mongo中的代理读取到内存中
        self.proxies = db["proxies"].find({"is_support_https": "支持"}).sort([("create_time", -1)]).limit(50)
        self.temp_list = []
        for p in self.proxies:
            proxy = "http://" + p["host"] + ":" + p["port"]
            print(proxy)
            test_res = request_test_proxy(p)
            if test_res:
                self.temp_list.append(proxy)
        # self.proxy = {
        #     "https": "http://47.103.117.209:3111",
        #     "http": "http://47.103.117.209:3111",
        # }

    def process_request(self, request, spider):
        """
        动态代理转发 给header添加Proxy-Authorization
        参考博客：
        https://blog.csdn.net/qq_26877377/article/details/82499087
        https://my.oschina.net/chenmoxuan/blog/3095926
        :param request:
        :param spider:
        :return:
        """
        # request.meta['proxy'] = 'http://forward.xdaili.cn:80'
        # timestamp = str(int(time.time()))  # timestamp
        # plan_text = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        # md5_string = hashlib.md5(plan_text.encode('utf-8')).hexdigest()  # sign
        # sign = md5_string.upper()
        # proxyAuth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp
        # 动态转发代理
        # request.headers["Proxy-Authorization"] = proxyAuth
        # request.meta["verify"] = False
        # request.meta["allow_redirects"] = False
        # 静态代理
        # request.meta['proxy'] = self.proxy["https"]
        request.meta['proxy'] = random.choice(self.temp_list)


class RedirectAddProxyDownloaderMiddleware(object):
    """
    自动代理下载中间件 (反爬重定向时，添加代理)
    博客参考： https://www.cnblogs.com/my8100/p/scrapy_middleware_autoproxy.html
    (1) 参考原生 redirect.py 模块，满足 dont_redirect 或 handle_httpstatus_list 等条件时，直接传递 response
    (2) 不满足条件(1)，如果响应状态码为 302 或 403，使用代理重新发起请求
    (3) 使用代理后，如果响应状态码仍为 302 或 403，直接丢弃

    想要改良：
    即当代理失效时，重新分配代理去请求
    """
    def __init__(self, settings):
        self.proxy_status = settings.get('PROXY_STATUS', [302, 403])
        # See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=proxy#module-scrapy.downloadermiddlewares.httpproxy
        self.proxy_config = settings.get('PROXY_CONFIG', 'http://username:password@some_proxy_server:port')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            settings=crawler.settings
        )

        # See /site-packages/scrapy/downloadermiddlewares/redirect.py

    def process_response(self, request, response, spider):
        if (request.meta.get('dont_redirect', False) or
                response.status in getattr(spider, 'handle_httpstatus_list', []) or
                response.status in request.meta.get('handle_httpstatus_list', []) or
                request.meta.get('handle_httpstatus_all', False)):
            return response

        if response.status in self.proxy_status:
            if 'Location' in response.headers:
                location = safe_url_string(response.headers['location'])
                redirected_url = urljoin(request.url, location)
            else:
                redirected_url = ''

            # AutoProxy for first time
            if not request.meta.get('auto_proxy'):
                request.meta.update({'auto_proxy': True, 'proxy': self.proxy_config})
                new_request = request.replace(meta=request.meta, dont_filter=True)
                new_request.priority = request.priority + 2

                spider.log('Will AutoProxy for <{} {}> {}'.format(
                    response.status, request.url, redirected_url))
                return new_request

            # IgnoreRequest for second time
            else:
                spider.logger.warn('Ignoring response <{} {}>: HTTP status code still in {} after AutoProxy'.format(
                    response.status, request.url, self.proxy_status))
                raise IgnoreRequest

        return response


class AutoChangeProxyDownloaderMiddleware(object):
    def __init__(self, settings):
        # 将redis的代理池，读取到内存中
        # TODO 将代理存入redis
        self._proxies = redis_conn.smembers("proxies")
        self.proxy_status = settings.get('PROXY_STATUS', [302, 403])
        # self.proxy_config = settings.get('PROXY_CONFIG', random.choice(list(self._proxies)).decode())
        # self.chromedriver = ChromeDriver()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    def process_request(self, request, spider):
        """
        请求前执行
        添加代理
        :param request:
        :param spider:
        :return:
        """
        request.meta['proxy'] = random.choice(list(self._proxies)).decode() if self._proxies else ""

    def process_response(self, request, response, spider):
        """
        请求后执行
        当重定向或者403时，重新分配代理构建请求对象去请求
        :param request:
        :param response:
        :param spider:
        :return:
        """
        if response.status in [200, 301]:
            print("[200 OK]")
            return response

        if response.status in self.proxy_status:
            # 当重定向或者403时，重新分配代理构建请求对象去请求
            # spider.logger.info('Response 302 or 403, Change proxy')
            print("Response 302 or 403, Change proxy")
            request.meta.update({'proxy': random.choice(list(self._proxies)).decode()}) if self._proxies else ""
            new_request = request.replace(meta=request.meta, dont_filter=True)
            new_request.priority = request.priority + 2
            return new_request

    def process_exception(self, request, exception, spider):
        """
        在请求错误时执行
        在此更换代理

        博客参考： https://www.cnblogs.com/lei0213/p/7904994.html
        :param request:
        :param response:
        :param spider:
        :return:
        """
        # spider.logger.info('Try Request Exception, Change proxy')
        print("Try Request Exception, Change proxy")
        proxy = random.choice(list(self._proxies)).decode() if self._proxies else ""
        spider.logger.debug(proxy)
        request.meta['proxy'] = proxy
