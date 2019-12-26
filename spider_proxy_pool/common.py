#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 19-12-23 下午8:12
# @Description:
import requests
from scrapy.utils.project import get_project_settings
from selenium import webdriver

settings = get_project_settings()


def request_test_proxy(item):
    """
    请求测试ip
    :param host:
    :param port:
    :return:
    """
    try:
        if item["is_support_https"] == "支持":
            response = requests.get("https://www.baidu.com/?tn=06074089_21_pg",
                                    proxies={"https": "http://" + item["host"] + ":" + item["port"]})
            if response.status_code == 200:
                return True
            else:
                return False
    except:
        return False


class ChromeDriver(object):
    """
    设计一个单例，给Middleware解析用

    chrome浏览器的options参数：
    https://blog.csdn.net/xc_zhou/article/details/82415870
    """
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.chrome_options.binary_location = '/opt/google/chrome/chrome'
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
        # self.chrome_options.add_argument("--proxy-server=47.103.117.209:3111")    # 固定代理,用于发帖用途
        # self.chrome_options.add_argument('--headless')  # 增加无界面选项
        # self.chrome_options.add_experimental_option('prefs', {"profile.managed_default_content_settings.images": 2})  # 不加载图片
        self.chrome_options.add_argument(
            "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'")
        # self.chrome_options.add_argument('Proxy-Authorization=%s' % auth)
        # from pyvirtualdisplay import Display
        # self.display = Display(visible=0, size=(800, 800))
        # self.display.start()
        self.driver = webdriver.Chrome(executable_path=settings["CHROMEDRIVER_PATH"], chrome_options=self.chrome_options)
