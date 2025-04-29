#!/usr/bin/python3
# -*- coding: utf-8 -*-            
"""
@Time : 2025/4/26 13:16
"""
import json


class SpiderPlatformApi:
    def __init__(self, seed_path=None):
        if seed_path:
            with open(seed_path, encoding="utf-8") as json_file:
                self.worker_stat = json.load(json_file)

    def get_all_seeds_with_trace(self):
        seeds = self.worker_stat["cur_task"]["seeds"]
        traces = self.worker_stat["cur_task"].get("traces", [])
        if not traces:
            traces = []
            for _ in seeds:
                traces.append({"id": "404"})
        return zip(seeds, traces)

    @property
    def sys_meta(self):
        return self.worker_stat["cur_task"]["_sys_meta"]

    # @property
    # def trace_info(self):
    #     return self.worker_stat["cur_task"]["trace_info"]

    @property
    def job_id(self):
        return self.sys_meta["job_id"]
