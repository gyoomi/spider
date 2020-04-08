#!/usr/bin/python
# -*- coding: UTF-8 -*-
from threading import Thread

"""
gil是cPython的产物， == java和jvm， jPython pypy

	1. 既然gil保证安全，但是gil又有时间片轮的概念
	2. gil会保证字节码的安全
"""

total = 0


def add():
	global total

	for i in range(10000000):
		total += 1


def desc():
	global total

	for i in range(10000000):
		total -= 1


if __name__ == '__main__':
	t1 = Thread(target=add)
	t2 = Thread(target=desc)
	t1.start()
	t2.start()

	t1.join()
	t2.join()

	print("total = " + str(total))

	print("OK")

