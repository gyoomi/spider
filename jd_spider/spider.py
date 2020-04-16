#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from scrapy import Selector


def parse_good(good_id):
    good_url = "https://item.jd.com/{}.html".format(good_id)
    good_html = requests.get(good_url).text
    sel = Selector(text=good_html)

    good_name = sel.xpath("//div[@class='sku-name']/text()").extract_first()

    """jd做了反扒。此方法行不通"""
    print(good_name)


if __name__ == '__main__':
    parse_good(10088444019)
