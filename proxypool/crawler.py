# -*- coding: utf-8 -*-
import re

import requests
from lxml import etree
import time
import pyquery as pq


class CrawlerMetaclass(type):
    """
    这是一个元类，用来对一个类的实例进行扩展
    """

    def __new__(cls, name, bases, attrs):
        attrs['__CrawlFuncCount__'] = 0
        attrs['__CrawlFuncList__'] = []
        for k, v in attrs.items():
            if 'crawl_' in str(k):
                attrs['__CrawlFuncList__'].append(k)
                attrs['__CrawlFuncCount__'] += 1
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=CrawlerMetaclass):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }

    def get_page(self, url, option=None):
        """
        获取要爬取页面的网页源代码
        :param url:要抓取页面的url
        :param option:headers的特殊选项
        :return:获取到的网页源代码
        """
        headers = self.headers if not option else dict(self.headers, **option)
        print('正在爬取：', url)
        try:
            response = requests.get(url, headers=headers)
            print('抓取成功：', url, response.status_code)
            if response.status_code == 200:
                return response.text
        except requests.exceptions.ConnectionError:
            print('抓取失败：', url)
            return None


    def get_proxies(self, func):
        proxies = []
        for proxy in eval('self.{}()'.format(func)):
            print('成功获取到代理：', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_ip3366(self):
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = self.get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')
            time.sleep(1)

    def crawl_kuaidaili(self):
        for i in range(1, 4):
            url = "https://www.kuaidaili.com/free/inha/%d/" % i
            response = self.get_page(url)
            if response:
                html = etree.HTML(response)
                trs = html.xpath('//div[@id="list"]/table//tr')[1:]
                for tr in trs:
                    ip = tr.xpath('./td[1]/text()')[0]
                    port = tr.xpath('./td[2]/text()')[0]
                    yield '{}:{}'.format(ip, port)
            time.sleep(1)
