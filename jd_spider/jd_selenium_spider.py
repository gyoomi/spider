#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import json
import re

from jd_spider.models import *


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy import Selector

chrome_options = Options()
# 设置无头模式
chrome_options.add_argument("--headless")
# 官方文档推荐，用来规避一些错误
chrome_options.add_argument("--disable-gpu")
# 设置不加载图片
chrome_options.add_argument("blink-settings=imagesEnabled=false")
browser = webdriver.Chrome(executable_path="D:/programs/dev/chromedriver_win32/chromedriver.exe", chrome_options=chrome_options)


def parse_good(good_id):
    try:
        browser.get("https://item.jd.com/{}.html".format(good_id))
        sel = Selector(text=browser.page_source)

        name = "".join(sel.xpath("//div[@class='sku-name']/text()").extract()).strip()
        price = float("".join(sel.xpath("//span[@class='price J-p-{}']/text()".format(good_id)).extract()).strip())
        content = "".join(sel.xpath("//div[@id='detail']//div[@class='tab-con']").extract_first().strip())
        image_list = sel.xpath("//div[@id='spec-list']//img/@src").extract()
        supplier = "".join(sel.xpath("//div[@id='summary-service']/text()").extract())

        comment_ele = browser.find_element_by_xpath("//li[@data-anchor='#comment']")
        comment_ele.click()
        time.sleep(10)

        sel = Selector(text=browser.page_source)
        #good_rate = int(sel.xpath("//div[@class='percent-con']/text()").extract()[0])
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
        good.good_rate = 0
        good.comment_nums = get_number(comment_nums)
        good.has_image_comment_nums = get_number(has_image_comment_nums)
        good.has_video_comment_nums = get_number(has_video_comment_nums)
        good.has_add_comment_nums = get_number(has_add_comment_nums)
        good.good_comment_nums = get_number(good_comment_nums)
        good.middle_comment_nums = get_number(middle_comment_nums)
        good.bad_comment_nums = get_number(bad_comment_nums)

        has_exist_in_db = Good.select().where(Good.id == good.id)
        if has_exist_in_db:
            good.save()
        else:
            good.save(force_insert=True)

        """处理商品评论标签汇总"""
        for tag in tag_list:
            matched = re.match("(.*)\((\d+)\)", tag)
            if matched:
                tag_name = matched.group(1)
                tag_nums = matched.group(2)
                has_exist_in_db = GoodEvaluateSummary.select().where(GoodEvaluateSummary.good == good, GoodEvaluateSummary.tag == tag_name)
                if has_exist_in_db:
                    summary = has_exist_in_db[0]
                else:
                    summary = GoodEvaluateSummary(good=good)

                summary.tag = tag_name
                summary.num = tag_nums
                summary.save()
        """处理商品的评论"""
        print("ok")
    finally:
        browser.quit()
        # browser.close()


def get_number(s):
    match = re.search("(\d+)", str(s))
    if match:
        return int(match.group(0))


if __name__ == '__main__':
    parse_good(100011386554)
    # print(get_number("400+"))
    pass
