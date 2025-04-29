#!/usr/bin/python3
# -*- coding: utf-8 -*-            
"""
@Time : 2025/4/25 16:46
"""
from pydantic import BaseModel


class SeedItem(BaseModel):
    seed: dict = dict()
    trace_info: dict = dict()
    meta: dict = dict()
    priority: int = 0


class TraceInfo(BaseModel):
    """
      {
                "id": uuid.uuid4().hex[:6],
                "job_id": job_id,
                "in_ts": int(time.time()),
                "scheduled_recv_ts": int(time.time()),
                "write_storage_ts": int(time.time()),
                "schedule_ts": int(time.time()),
                "already_retry_num": 0,
            }
    """
    trace_id: str = ""
    job_id: str = ""
    priority: int = 0
    in_ts: int = 0
    scheduled_recv_ts: int = 0
    write_storage_ts: int = 0
    schedule_ts: int = 0
    already_retry_num: int = 0
    trace_info: dict = dict()
