#!/usr/bin/python
# -*- coding: UTF-8 -*-

from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED, as_completed
import time


def sleep_task(sleep_time, task_name):
    print("{} sleep {} s".format(task_name, sleep_time))
    time.sleep(sleep_time)
    print("{} end".format(task_name))


thread_pool = ThreadPoolExecutor(max_workers=2)
feature01 = thread_pool.submit(sleep_task, 2, "task001")
feature02 = thread_pool.submit(sleep_task, 3, "task002")
feature03 = thread_pool.submit(sleep_task, 4, "task003")

print(feature01.cancel())
print(feature02.cancel())
print(feature03.cancel())

print("main end!!!")
