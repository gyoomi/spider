#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import pickle


def login():
    url = "https://accounts.douban.com/j/mobile/login/basic"
    form_data = {
        "ck": "",
        "name": "18392889591",
        "password": "123456!",
        "remember": "false",
        "ticket": ""
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }

    resp = requests.post(url, data=form_data, headers=headers)
    result = json.loads(resp.text)

    if result["status"] == "success":
        print("登录ok")
    else:
        print("登录failure")

    cookie_jar = resp.cookies
    with open("douban.cookie", "wb") as f:
        pickle.dump(cookie_jar, f)

    print("ok")


if __name__ == '__main__':
    login()
