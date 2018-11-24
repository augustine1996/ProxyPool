# -*- coding: utf-8 -*-
from .crawler import Crawler
from .db import RedisClient
from .setting import *


class Downloader():
    def __init__(self):
        self.crawler = Crawler()
        self.redis = RedisClient()

    def is_poll_full(self):
        """
        判断代理池是否已满
        :return: 返回一个布尔值
        """
        if self.redis.count() >= POOL_COUNT:
            return True
        else:
            return False

    def run(self):
        if not self.is_poll_full():
            for func in range(self.crawler.__CrawlFuncCount__):
                func = self.crawler.__CrawlFuncList__[func]
                for proxy in self.crawler.get_proxies(func):
                    self.redis.add_to_redis(proxy)
