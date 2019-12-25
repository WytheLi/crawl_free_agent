#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 19-12-24 下午1:42
# @Description:
import requests

# url = "https://ip.ihuan.me/"
url = "https://www.baidu.com"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

res = requests.get(url, headers=headers, proxies={"http": "http://153.101.64.50:12034"})
print(res.text)
print(res.status_code)
