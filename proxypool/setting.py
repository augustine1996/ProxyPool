# -*- coding: utf-8 -*-
# 设置下载器状态
DOWNLOADER_ENABLED = True

# 设置测试器状态
TESTER_ENABLED = True

# 设置API状态
API_ENABLED = True

# 设置过滤代理的间隔时间
TEST_INTERVAL = 30

# 设置获取代理的间隔时间
DOWNLOAD_INTERVAL = 300

# 设置API的主机地址、端口
API_HOST = '127.0.0.1'
API_PORT = 5000

# Redis数据库地址、端口、密码
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None

# 设置代理池的最大总数
POOL_COUNT = 500

# 设置代理分数
MAX_SCORE = 20
MIN_SCORE = 0
INITIAL_SCORE = 10

# 设置代理池在redis中的键
REDIS_KEY = 'proxies'

# 设置状态码范围
VALID_STATUS_CODES = [200, 302]

# 测试代理IP的网址
TEST_URL = 'http://www.baidu.com'

# 设置一次测试的数量
TEST_SIZE = 10
