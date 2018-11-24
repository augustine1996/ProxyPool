# -*- coding: utf-8 -*-
import random
import re

import redis
from .setting import *


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化RedisClient的实例
        :param host:redis数据库地址
        :param port:redis数据库端口
        :param password:redis数据库密码，默认为None
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add_to_redis(self, proxy, scroe=INITIAL_SCORE):
        """
        添加代理到redis数据库，设置分数为INITIAL_SCORE
        :param proxy: 代理
        :param scroe: 初始分数
        """
        if not re.match(r'\d+.\d+.\d+.\d+:\d+', proxy):
            print('代理不符合规范：', proxy, '丢弃！')
        self.db.zadd(REDIS_KEY, {proxy: scroe})

    def count(self):
        """
        获得redis数据库中代理的数量
        :return:代理数量
        """
        return self.db.zcard(REDIS_KEY)

    def set_max_scroe(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        """
        self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def decrease(self, proxy):
        """
        代理分数减一分，小于MIN_SCORE则删除
        :param proxy: 代理
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            self.db.zrem(REDIS_KEY, proxy)

    def batch(self, start, stop):
        """
        批量获取代理
        :param start:开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)

    def random(self):
        """
        随机获得一个代理
        :return: 随机代理
        """
        results = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(results):
            return random.choice(results)
        else:
            results = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(results):
                return random.choice(results)
            else:
                return None
