# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/20 10:37
@Author  : jayden
"""
import threading
import time
from test.spiders.settings.airspider_settings import SpiderSettings

import scrawlpy
from scrawlpy import Spider
from scrawlpy.core.crawl import CrawlerProcess
from scrawlpy.items.result import Result
from scrawlpy.utils.gen_seed import write_seed_json_file


class Myspider(scrawlpy.AirSpider):
    Settings = SpiderSettings
    __custom_setting__ = {
        "Timeout": "5",
        "KEEP_ALIVE": False,
    }

    def start_task_distribute(self) -> None:
        """
        分发任务
        Returns:

        """
        while True:
            self.request_queue.add({"url": "https://www.baidu.com"}, 1)
            # self.request_queue.add({"url": "https://www.qq.com"}, 2)

    def start_requests(self, seed):
        # print(seed)
        priority, seed = seed
        # self.log.info()
        url = seed.get("url")
        self.logger.info(f"线程id: {threading.get_ident()} 超时时间: {self.settings.Timeout}")
        res = self.requests.get(url)
        # self.logger.info(res.text)
        # for i in range(10):
        #     yield Request("http://www.baidu.com", callback=self.parse)
        # res = self.requests.get("http://www.baidu.com")
        # print(res.text)


# 示例使用
class ExampleSpider(Spider):
    custom_settings = {
        "max_works": 20,
    }

    def start_requests(self, request):
        self.logger.info(f"seed: {request}")
        self.logger.info(self.scheduler.spider_platform_api.job_id)
        size = self.scheduler.queue.size()
        self.logger.info(f"size: {size} thread_id: {threading.get_ident()}")
        self.scheduler.add_seed("http://www.cip.com", 10)
        response = self.requests.get("http://www.baidu.com")
        print(response.text)
        # 模拟网络io
        time.sleep(0.4)
        result = {
            "url": "http://www.baidu.com",
            "data": "123",
        }
        return Result(result=result, status_code=200)


def run_spider(**kwargs):
    process = CrawlerProcess(SpiderSettings())
    max_works = 21
    # process.settings.set("max_works", 21)
    process.settings.set("max_works", max_works)
    process.crawl(ExampleSpider, **kwargs)
    process.start(runtime_limit=3)  # 设置爬虫运行时间限制，比如10秒


if __name__ == "__main__":
    import json

    test_seeds = [json.dumps({"url": "https://httpbin.org/get"}), json.dumps({"url": "https://httpbin.org/ip"})]
    run_spider(seed_path=write_seed_json_file(test_seeds, ExampleSpider.spider_name))
