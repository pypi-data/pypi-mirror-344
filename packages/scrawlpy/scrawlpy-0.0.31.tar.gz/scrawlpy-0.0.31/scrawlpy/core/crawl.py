# -*- coding: utf-8 -*-            
# @Time : 2025/4/25 11:54
import threading
import time

from typing_extensions import Optional, Union

from scrawlpy.core.metrics import Metrics
from scrawlpy.core.scheduler import Scheduler
from scrawlpy.setting import Settings
from scrawlpy.core.spiders.base_spider import AbstractSpider


class Crawler:
    def __init__(self, spider_class, settings=None, **kwargs):
        self.settings = settings or Settings()
        seed_path = kwargs.get("seed_path")
        self.scheduler = Scheduler(self.settings, seed_source='file', seed_path=seed_path)
        self.spider: AbstractSpider = spider_class(scheduler=self.scheduler, settings=settings, **kwargs)
        _settings = self.spider.settings
        self.middlewares = self.spider.middlewares
        self.pipelines = self.spider.pipelines
        self.shutdown_event = threading.Event()
        self.distribute_shutdown_event = threading.Event()
        self.metrics = Metrics(self.spider.settings)

    def crawl(self, request):
        try:
            for middleware, _ in self.middlewares:
                request = middleware.pre_process(request)

            response = self.spider.start_requests(request)

            if response:
                for middleware, _ in self.middlewares:
                    response = middleware.after_process(response)
                # metrics.record_seed_status(request.seed, "success")
                # metrics.complete()
                # print(f"Request completed in {metrics.execution_time()} seconds")
                item = self.spider.parse(response)
                for pipeline, _ in self.pipelines:
                    pipeline.process_item(item, self.spider)
                return item
            else:
                self.metrics.record_seed_status(request.url, "failure")
        except Exception as e:
            for middleware, _ in self.middlewares:
                middleware.except_process(e)
            self.metrics.record_seed_status(request.url, "failure")
            return None

    def start_crawl(self, runtime_limit):
        seed_thread = threading.Thread(target=self.scheduler.load_seeds, args=(self.shutdown_event,))
        seed_thread.start()

        threads = []
        for _ in range(self.spider.settings.get("max_works", 10)):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)

        start_time = time.time()
        while time.time() - start_time < runtime_limit:
            if self.distribute_shutdown_event.is_set() or self.shutdown_event.is_set():
                break
            time.sleep(1)

        self.shutdown_event.set()
        self.spider.logger.info("Spider ready to stop, waiting for 5 seconds...")
        time.sleep(5)
        self.spider.logger.info("Spider stopped...")
        self.distribute_shutdown_event.set()

        for t in threads:
            t.join()

    def worker(self):
        while not self.distribute_shutdown_event.is_set():
            request = self.scheduler.get_request()
            if request:
                self.crawl(request)
            elif self.shutdown_event.is_set():
                break
            else:
                time.sleep(0.1)


class CrawlerProcess:
    def __init__(self, settings: Union[Settings, dict] = None):
        self.settings = settings or Settings()
        self.crawlers = []

    def crawl(self, spider_class, **kwargs):
        crawler = Crawler(spider_class, settings=self.settings, **kwargs)
        self.crawlers.append(crawler)

    def start(self, runtime_limit=None):
        for crawler in self.crawlers:
            crawler.start_crawl(runtime_limit)
