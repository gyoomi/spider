#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import json

from jd_spider.models import *


from selenium import webdriver
from scrapy import Selector

browser = webdriver.Chrome(executable_path="D:/programs/dev/chromedriver_win32/chromedriver.exe")


def parse_good(good_id):
    browser.get("https://item.jd.com/{}.html".format(good_id))
    sel = Selector(text=browser.page_source)

    name = "".join(sel.xpath("//div[@class='sku-name']/text()").extract())
    price = float("".join(sel.xpath("//span[@class='price J-p-{}']".format(good_id)).extract()).strip())
    content = "".join(sel.xpath("//div[@id=''detail]//div[@class='tab-con']").extract())
    image_list = sel.xpath("//div[@id='spec-list']/image/@src").extract()
    supplier = "".join(sel.xpath("//div[@id='summary-service']/text()").extract())

    comment_ele = browser.find_element_by_xpath("//li[@data-anchor='#comment']")
    comment_ele.click()
    time.sleep(4)

    sel = Selector(text=browser.page_source)
    good_rate = int(sel.xpath("//div[@class='percent-con']").extract()[0])
    tag_list = sel.xpath("//div[@class='tag-list tag-available']//span/text()").extract()
    comment_nums = sel.xpath("//ul[@class='filter-list']/li[@clstag='shangpin|keycount|product|allpingjia']/@data-num").extract()[0]
    has_image_comment_nums = sel.xpath("//ul[@class='filter-list']/li[@clstag='shangpin|keycount|product|shaidantab']/@data-num").extract()[0]
    has_video_comment_nums = sel.xpath("//ul[@class='filter-list']/li[@clstag='shangpin|keycount|product|pingjiashipin']/@data-num").extract()[0]
    has_add_comment_nums = sel.xpath("//ul[@class='filter-list']/li[@clstag='shangpin|keycount|product|zhuiping']/@data-num").extract()[0]
    good_comment_nums = sel.xpath("//ul[@class='filter-list']/li[@clstag='shangpin|keycount|product|haoping']/@data-num").extract()[0]
    middle_comment_nums = sel.xpath("//ul[@class='filter-list']/li[@clstag='shangpin|keycount|product|zhongping']/@data-num").extract()[0]
    bad_comment_nums = sel.xpath("//ul[@class='filter-list']/li[@clstag='shangpin|keycount|product|chaping']/@data-num").extract()[0]

    good = Good()
    good.id = good_id
    good.name = name
    good.content = content
    good.price = price
    good.image_list = json.dumps(image_list)
    good.supplier = supplier
    good.good_rate = good_rate
    good.comment_nums = comment_nums
    good.has_image_comment_nums = has_image_comment_nums
    good.has_video_comment_nums = has_video_comment_nums
    good.has_add_comment_nums = has_add_comment_nums
    good.good_comment_nums = good_comment_nums
    good.middle_comment_nums = middle_comment_nums
    good.bad_comment_nums = bad_comment_nums

    has_exist_in_db = Good.select().where(Good.id == good.id)
    if has_exist_in_db:
        good.save()
    else:
        good.save(force_insert=True)


if __name__ == '__main__':
    pass
