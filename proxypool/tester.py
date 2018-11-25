# -*- coding: utf-8 -*-
import time

import requests

from .db import RedisClient
from .setting import *
from threading import Thread
from queue import Queue


class Tester():
    def __init__(self):
        self.redis = RedisClient()

    def use_thread_test(self, test_proxies):
        """
        使用多线程进行代理的可用性测试
        :param test_proxies:要测试的代理列表
        """
        test_count = len(test_proxies)
        proxy_queue = Queue(test_count)
        for i in range(test_count):
            proxy_queue.put(test_proxies[i])
        for i in range(5):
            t = TestThread(proxy_queue)
            t.start()

    def run(self):
        try:
            count = self.redis.count()
            print('代理池中当前共有：%d 个代理' % count)
            for i in range(0, count, TEST_SIZE):
                start, stop = i, min(i + TEST_SIZE, count)
                test_proxies = self.redis.batch(start, stop)
                self.use_thread_test(test_proxies)
                time.sleep(3)
        except Exception as e:
            print('测试器发生错误：', e.args)


class TestThread(Thread):
    def __init__(self, proxy_queue, *args, **kwargs):
        super(TestThread, self).__init__(*args, **kwargs)
        self.proxy_queue = proxy_queue
        self.redis = RedisClient()

    def run(self):
        while True:
            if self.proxy_queue.empty():
                break
            proxy = self.proxy_queue.get()
            try:
                resp = requests.get(url=TEST_URL, proxies={'http': proxy}, timeout=5)
                if resp.status_code in VALID_STATUS_CODES:
                    self.redis.set_max_scroe(proxy)
                    print('代理可用：', proxy)
                else:
                    self.redis.decrease(proxy)
                    proxy('请求响应码不合法：', resp.status_code, 'IP', proxy)
            except:
                self.redis.decrease(proxy)
                print('代理请求失败：', proxy)
