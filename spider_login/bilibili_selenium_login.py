#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time

from selenium import webdriver

url = "https://passport.bilibili.com/login"
browser = webdriver.Chrome(executable_path="D:/programs/dev/chromedriver_win32/chromedriver.exe")


def login():
    username = ""
    password = ""

    browser.get(url)
    # 很重要
    browser.maximize_window()

    username_ele = browser.find_element_by_xpath("//input[@id='login-username']")
    password_ele = browser.find_element_by_xpath("//input[@id='login-passwd']")
    username_ele.send_keys(username)
    password_ele.send_keys(password)

    """ 1. 鼠标移动到正确的元素上，显示出没有缺口的图片并下载 """
    pass


if __name__ == '__main__':
    print("ok")
    pass
