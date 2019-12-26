#### 爬取地址
[小幻代理](https://ip.ihuan.me/)

#### 项目环境
系统：  linux / win
数据库： [mongodb](https://docs.mongodb.com/v4.0/tutorial/install-mongodb-on-ubuntu/)  
python依赖库： pip3 install -r requirements.txt


#### 爬虫启动
```sh
# 手动启动
python3 run.py

# 定时启动 一个小时爬取一次
sudo crontab -e
# 添加下面这句 (python解释器地址 执行脚本地址 >> 日志文件地址)
* */3 * * * cd /home/wytheli/Desktop/spider_proxy_pool&&/home/wytheli/.virtualenvs/mn_spider/bin/python3 /home/wytheli/Desktop/spider_proxy_pool/run.py >> /home/wytheli/Desktop/spider_proxy_pool/logs/scrapy_spider_proxies.log
*/30 * * * * cd /home/wytheli/Desktop/spider_proxy_pool&&/home/wytheli/.virtualenvs/mn_spider/bin/python3 /home/wytheli/Desktop/spider_proxy_pool/cache_proxies.py >> /home/wytheli/Desktop/spider_proxy_pool/logs/cache_proxies.log

* */4 * * * cd /root/spider_proxy_pool&&/root/.virtualenvs/mn_spider/bin/python3 /root/spider_proxy_pool/run.py >> /root/spider_proxy_pool/logs/scrapy_spider_proxies.log
*/30 * * * * cd /root/spider_proxy_pool&&/root/.virtualenvs/mn_spider/bin/python3 /root/spider_proxy_pool/cache_proxies.py >> /root/spider_proxy_pool/logs/cache_proxies.log


service cron restart
```

#### redis缓存代理
需要不重复的数据，所以使用集合
- 数据类型 有序集合
```txt
# redis-server v3.0.6 v4.0.9亲测
# 添加一条或者多条
redis_conn.zadd("proxies", {"aaa": 1, "bbb": 2, "ccc": 3})
# 删除一条或者多条
redis_conn.zrem("proxies", "aaa", "bbb")
# 取出指定区间的集合数据
redis_conn.zrange("proxies", 0, -1)
```

- 无序集合
```txt
res_sadd = redis_conn.sadd("set_test", "aaa", "bbb")
redis_conn.srem("set_test", "aaa")
res_smembers = redis_conn.smembers("set_test")

```

- 列表
```txt
redis_conn.lpush("list_test", "aaa", "bbb")
redis_conn.lrange("list_test", 0, -1)
```

#### 利用tornado.httpclient或aiohttp异步筛选可用代理


#### OCR识别，tessersor模块破解简单验证码
- Tesseract的安装使用 Tesseract是OCR的一个库  
    - 博客参考： https://blog.csdn.net/jclian91/article/details/80628188
    - 安装Tesseract：
    ```sh
    sudo apt-get tesseract-ocr
    ```
    - 安装Tesseract python客户端
    ```sh
    pip3 install pytesseract
    ```
    - tesserocr
    ```sh
    pip3 install tesserocr
    ```
