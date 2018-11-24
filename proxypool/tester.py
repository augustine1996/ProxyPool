# -*- coding: utf-8 -*-
import time
import asyncio

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
import aiohttp
from .db import RedisClient
from .setting import *


class Tester():
    def __init__(self):
        self.redis = RedisClient()

    async def test_one_proxy(self, proxy):
        """
        异步测试单个代理
        :param proxy: 要测试的代理
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy.decode('utf-8')
                cur_proxy = 'http://' + proxy
                print('当前正在测试：', proxy)
                async with session.get(TEST_URL, proxy=cur_proxy, timeout=10, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.set_max_scroe(proxy)
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法：', response.status, 'IP:', proxy)
            except (
                    ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败：', proxy)

    def run(self):
        try:
            count = self.redis.count()
            print('代理池中当前共有：%d 个代理' % count)
            for i in range(0, count, TEST_SIZE):
                start, stop = i, min(i + TEST_SIZE, count)
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_one_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(3)
        except Exception as e:
            print('测试器发生错误：', e.args)
