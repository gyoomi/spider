#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
from threading import Thread

"""
创建线程的两种方法：
	1. 实例化Thread类
	2. 继承Thread类
"""


def sleep_task(sleep_time):
	print("sleep {} start...".format(sleep_time))
	time.sleep(sleep_time)
	print("sleep {} end...".format(sleep_time))


if __name__ == '__main__':
	t1 = Thread(target=sleep_task, args=(2,))
	t2 = Thread(target=sleep_task, args=(3,))

	t1.start()
	t2.start()

	print("[OVER]")
