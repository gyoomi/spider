#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time

from selenium import webdriver

url = "https://www.douban.com/"
browser = webdriver.Chrome(executable_path="D:/programs/dev/chromedriver_win32/chromedriver.exe")


def login():
    try:
        username = "18392889591"
        password = "123456!"

        browser.get(url)
        browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
        login_ele = browser.find_element_by_xpath("//li[@class='account-tab-account']")
        login_ele.click()

        username_ele = browser.find_element_by_xpath("//input[@id='username']")
        password_ele = browser.find_element_by_xpath("//input[@id='password']")
        username_ele.send_keys(username)
        password_ele.send_keys(password)

        submit_ele = browser.find_element_by_xpath("//a[@class='btn btn-account btn-active']")
        submit_ele.click()

        cookies = browser.get_cookies()
        print(cookies)
    finally:
        time.sleep(10)
        browser.quit()
        pass


if __name__ == '__main__':
    login()
    print("over")
    pass
