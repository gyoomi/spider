#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

"""
创建线程的两种方法：
	1. 实例化Thread类
	2. 继承Thread类
"""


class SleepThread(Thread):

	def __init__(self, sleep_time):
		""" 构造器 """
		super().__init__()
		self.sleep_time = sleep_time

	def run(self):
		"""
		重写run()方法
		"""
		print("{} sleep {} start...".format(self.name, self.sleep_time))
		time.sleep(self.sleep_time)
		print("{} sleep {} end...".format(self.name, self.sleep_time))
		pass


if __name__ == '__main__':
	t1 = SleepThread(2)
	t2 = SleepThread(4)
	t1.start()
	t2.start()

	print("[OVER]")
