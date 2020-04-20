#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time

from selenium import webdriver
from scrapy import Selector

browser = webdriver.Chrome(executable_path="D:/programs/dev/chromedriver_win32/chromedriver.exe")
browser.get("https://item.jd.com/10088444019.html")

# print(browser.page_source)
sel = Selector(text=browser.page_source)

print(sel.xpath("//span[@class='price J-p-{}']/text()".format(10088444019)).extract_first())
time.sleep(3)
browser.close()
