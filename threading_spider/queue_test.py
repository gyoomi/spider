#!/usr/bin/python
# -*- coding: UTF-8 -*-

from queue import Queue

if __name__ == '__main__':
    message_queue = Queue()
    message_queue.put("test111")
    message_queue.put("test222")
    message_queue.put("test333")
    
    print(message_queue.get())
    print(message_queue.get())
    print(message_queue.get())
    # 如果没有元素的，线程会阻塞在这里
    print(message_queue.get())
