import json
import time

from scrawlpy.items.seed import SeedItem
from scrawlpy.core.scheduler.priority_queue import PriorityQueue
from scrawlpy.sutils.platform_api import SpiderPlatformApi


class Scheduler:
    def __init__(self, settings, seed_source='file', seed_path=None):
        self.settings = settings
        self.queue = PriorityQueue()

        self.seed_source = seed_source
        self.seed_path = seed_path
        self.spider_platform_api = SpiderPlatformApi(self.seed_path)

    def start_task_distribute(self, shutdown_event) -> None:
        """
        分发任务
        Returns:

        """
        n = 0
        while not shutdown_event.is_set():
            # self.queue.put({"url": "https://www.baidu.com"}, )
            # self.queue.put({"url": "https://www.qq.com"}, )
            self.queue.put("https://www.baidu.com", 1)
            self.queue.put("https://www.baidu.com", 1)
            n += 2
            print('当前任务数: {}'.format(n))
            time.sleep(0.1)
        # self.logger.info(f"到超时时间了，任务分发结束...")

    def load_seeds(self, shutdown_event):
        if self.seed_source == 'file' and self.seed_path:
            seeds = self.spider_platform_api.get_all_seeds_with_trace()
            for seed, trace_info in seeds:
                try:
                    seed = json.loads(seed)
                except json.JSONDecodeError:
                    pass
                priority = trace_info.get("priority", 0)
                seed_item: SeedItem = SeedItem(seed=seed, trace_info=trace_info,
                                               meta={"sys_meta": self.spider_platform_api.sys_meta})
                self.queue.put(seed_item.model_dump_json(), priority)
            shutdown_event.set()
        else:
            self.start_task_distribute(shutdown_event)

    def add_seed(self, seed: any, priority: int = 0) -> None:
        """
        添加数据到优先级队列中
        Args:
            seed: 数据
            priority: 优先级，数字越小优先级越高
        """
        if isinstance(seed, SeedItem):
            seed_item = seed.model_dump_json()
        else:
            seed = {
                "seed": seed
            }
            seed_item = SeedItem(seed=seed, meta={"sys_meta": self.spider_platform_api.sys_meta}).model_dump_json()
        self.queue.put(seed_item, priority)

    def get_request(self):
        try:
            queue_data = self.queue.get(timeout=1)
            if queue_data:
                priority, seed = queue_data
                return SeedItem(**json.loads(seed))
        except self.queue.is_empty():
            return None
