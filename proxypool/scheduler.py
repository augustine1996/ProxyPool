# -*- coding: utf-8 -*-
import time
from multiprocessing import Process
from .api import app
from .downloader import Downloader
from .tester import Tester
from .setting import *


class Scheduler(object):
    def scheduler_tester(self, cycle=TEST_INTERVAL):
        """
        定时测试代理，筛选出可用的代理
        :param cycle: 每次过滤代理的间隔时间
        """
        tester = Tester()
        while True:
            print("测试器开始运行：")
            tester.run()
            time.sleep(cycle)

    def scheduler_downloader(self, cycle=DOWNLOAD_INTERVAL):
        """
        定时获取代理
        :param cycle:每次获取代理的间隔时间
        """
        downloader = Downloader()
        while True:
            print("下载器开始运行：")
            downloader.run()
            time.sleep(cycle)

    def scheduler_api(self):
        """
        开始API
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        print("代理池开始运行：")
        if TESTER_ENABLED:
            tester_process = Process(target=self.scheduler_tester)
            tester_process.start()

        if DOWNLOADER_ENABLED:
            downloader_process = Process(target=self.scheduler_downloader)
            downloader_process.start()

        if API_ENABLED:
            api_process = Process(target=self.scheduler_api)
            api_process.start()
