#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import ast
from urllib import parse
from datetime import datetime
from threading import Thread
from threading import Lock

import requests

from csdn_spider.models import *
from scrapy import Selector


http_prefix = "https://bbs.csdn.net/"
accessible_url_list = []


def get_nodes_json():
	left_menu_text = requests.get("https://bbs.csdn.net/dynamic_js/left_menu.js?csdn").text
	nodes_str_result = re.search("forumNodes: (.*])", left_menu_text)
	if nodes_str_result:
		nodes_str = nodes_str_result.group(1).replace("null", "None")
		nodes_list = ast.literal_eval(nodes_str)
		return nodes_list
	return []


def obtain_accessible_url(nodes_list):
	"""
	提取可访问的子菜单的url.
	结果 -> 包含顶级和儿子节点url
	"""

	for item in nodes_list:
		if "url" in item:
			if item["url"]:
				accessible_url_list.append(item["url"])
			if "children" in item:
				obtain_accessible_url(item["children"])


def obtain_root_url(nodes_list):
	root_urls = []
	"""
	获取顶级的菜单的url的集合
	"""
	for item in nodes_list:
		if "url" in item and item["url"]:
			root_urls.append(item["url"])

	return root_urls


def get_all_valid_children_url():
	all_valid_children_url = []

	nodes_list = get_nodes_json()
	obtain_accessible_url(nodes_list)
	root_urls_list = obtain_root_url(nodes_list)
	for item in accessible_url_list:
		if item not in root_urls_list:
			all_valid_children_url.append(item)

	return all_valid_children_url


def add_other_category_url():
	last_url = []

	"""
	获取需爬取的所有url
	"""
	all_valid_children_url = get_all_valid_children_url()
	for item in all_valid_children_url:
		last_url.append(parse.urljoin(http_prefix, item))
		last_url.append(parse.urljoin(http_prefix, item + "/recommend"))
		last_url.append(parse.urljoin(http_prefix, item + "/closed"))

	return last_url


class CsdnSpiderTask(Thread):
	http_prefix = "https://bbs.csdn.net/"
	author_http_prefix = "https://me.csdn.net/bbs/"
	urls = []

	def __init__(self, urls, topic_lock, answer_lock, author_lock):
		super().__init__()
		self.urls = urls
		self.topic_lock = topic_lock
		self.answer_lock = answer_lock
		self.author_lock = author_lock

	def run(self):
		for i in range(len(self.urls)):
			i += 1
			url_to_use = self.urls.pop()
			print(self.name + "线程处理 [" + str(url_to_use) + "] url链接")
			response_text = requests.get(url_to_use).text
			sel = Selector(text=response_text)

			# 没有帖子，则不进行下面的逻辑
			if sel.xpath("//table[@class='forums_tab_table']//tbody//tr[1]/td[1]/text()"):
				first_content = sel.xpath("//table[@class='forums_tab_table']//tbody//tr[1]/td[1]/text()").extract()[0]
				if "没有帖子" in first_content:
					continue
			self.parse_url(url_to_use)

	def parse_url(self, url):
		"""
		解析url下的数据并进行入库保存
			1. 发送请求获取列表页面信息
			2. 解析页面获取有效的行数据
			3. 解析行数据 -> topic answer author
			4. 保存相关数据
		"""
		response_text = requests.get(url).text
		sel = Selector(text=response_text)
		all_trs = sel.xpath("//table[@class='forums_tab_table']//tbody//tr")

		for tr in all_trs:
			topic = Topic()
			topic_url = ""
			author_url = ""

			if tr.xpath(".//td[1]/span/text()").extract():
				status = tr.xpath(".//td[1]/span/text()").extract()[0]
				topic.status = status
			if tr.xpath(".//td[2]/em/text()").extract():
				score = tr.xpath(".//td[2]/em/text()").extract()[0]
				topic.score = int(score)
			if tr.xpath(".//td[3]/a[contains(@class, 'forums_title')]/@href"):
				topic_url = tr.xpath(".//td[3]/a[contains(@class, 'forums_title')]/@href").extract()[0]
				topic_url = parse.urljoin(self.http_prefix, topic_url)
				topic_id = topic_url.split("/")[-1]
				topic.id = int(topic_id)
			if tr.xpath(".//td[3]/a[contains(@class, 'forums_title')]/text()"):
				topic_title = tr.xpath(".//td[3]/a[contains(@class, 'forums_title')]/text()").extract()[0]
				topic.title = topic_title
			if tr.xpath(".//td[4]/a/@href"):
				author_url = tr.xpath(".//td[4]/a/@href").extract()[0]
				author_id = author_url.split("/")[-1]
				author_url = parse.urljoin(self.author_http_prefix, author_id)
				topic.author_id = author_id
			if tr.xpath(".//td[4]/em/text()"):
				create_time_str = tr.xpath(".//td[4]/em/text()").extract()[0]
				create_time = datetime.strptime(create_time_str, "%Y-%m-%d %H:%M")
				topic.create_time = create_time
			if tr.xpath(".//td[5]/span/text()"):
				reply_text = tr.xpath(".//td[5]/span/text()").extract()[0]
				answer_nums = reply_text.split("/")[0]
				click_nums = reply_text.split("/")[1]
				topic.answer_nums = int(answer_nums)
				topic.click_nums = int(click_nums)
			if tr.xpath(".//td[6]/em/text()"):
				last_answer_time_str = tr.xpath(".//td[6]/em/text()").extract()[0]
				last_answer_time = datetime.strptime(last_answer_time_str, "%Y-%m-%d %H:%M")
				topic.last_answer_time = last_answer_time

			# 保存topic
			self.topic_lock.acquire()
			has_exist_in_db = Topic.select().where(Topic.id == topic.id)
			if has_exist_in_db:
				topic.save()
			else:
				topic.save(force_insert=True)
			self.topic_lock.release()

			self.parse_topic(topic_url)
			self.parse_author(author_url)

		if sel.xpath("//a[contains(@class,'pageliststy next_page') and contains(text(), '下一页')]/@href"):
			next_page_href = sel.xpath("//a[contains(@class,'pageliststy next_page') and contains(text(), '下一页')]/@href").extract()[0]
			next_page_url = parse.urljoin(self.http_prefix, next_page_href)
			self.parse_url(next_page_url)

	def parse_topic(self, topic_url):
		"""
		获取帖子的详情和回答
		"""

		topic_id = int(topic_url.split("/")[-1])

		response_text = requests.get(topic_url).text
		sel = Selector(text=response_text)
		all_divs = sel.xpath("//div[starts-with(@id, 'post-')]")
		# 一楼肯定是帖子内容,且肯定有内容
		topic = Topic()
		topic.id = topic_id

		if all_divs[0]:
			topic_item = all_divs[0]
			if topic_item.xpath(".//div[@class='post_body post_body_min_h']"):
				content = topic_item.xpath(".//div[@class='post_body post_body_min_h']").extract()[0]
				topic.content = content
			if topic_item.xpath(".//label[@class='red_praise digg']/em/text()"):
				praise_nums = topic_item.xpath(".//label[@class='red_praise digg']/em/text()").extract()[0]
				topic.praise_nums = int(praise_nums)
			if topic_item.xpath(".//div[@class='close_topic']/text()"):
				jtl_str = topic_item.xpath(".//div[@class='close_topic']/text()").extract()[0]
				jtl = 0.0
				jtl_match = re.search("(\\d+)%", jtl_str)
				if jtl_match:
					jtl = jtl_match.group(1)

				topic.jtl = float(jtl)

			# 更新帖子
			topic.save()

		""" 处理回答 """
		if len(all_divs) > 1:
			for answer_item in all_divs[1:]:
				answer = Answer()
				answer.topic_id = topic_id

				if answer_item.xpath(".//div[@class='nick_name']/a[1]/@href"):
					author_info = answer_item.xpath(".//div[@class='nick_name']/a[1]/@href").extract()[0]
					author_id = author_info.split("/")[-1]
					answer.author_id = author_id
				if answer_item.xpath(".//label[@class='date_time']/text()"):
					create_time_str = answer_item.xpath(".//label[@class='date_time']/text()").extract()[0]
					create_time = datetime.strptime(create_time_str, "%Y-%m-%d %H:%M:%S")
					answer.create_time = create_time
				if answer_item.xpath(".//div[@class='post_body post_body_min_h']"):
					content = answer_item.xpath(".//div[@class='post_body post_body_min_h']").extract()[0]
					answer.content = content
				if answer_item.xpath(".//label[@class='red_praise digg']/em/text()"):
					praise_nums = answer_item.xpath(".//label[@class='red_praise digg']/em/text()").extract()[0]
					answer.praise_nums = int(praise_nums)

				answer.save()

		if sel.xpath("//a[contains(@class,'pageliststy next_page') and contains(text(), '下一页')]/@href"):
			next_page_href = sel.xpath("//a[contains(@class,'pageliststy next_page') and contains(text(), '下一页')]/@href").extract()[0]
			next_page_url = parse.urljoin(self.http_prefix, next_page_href)
			# 解析第二页及之后的内容
			self.parse_topic_of_next_page(next_page_url, topic_id)

	def parse_topic_of_next_page(self, next_page_url_of_topic, topic_id):
		"""
			获取帖子回复中多页情况下，非第一页的详情回答
		"""

		topic_id = topic_id

		response_text = requests.get(next_page_url_of_topic).text
		sel = Selector(text=response_text)
		all_divs = sel.xpath("//div[starts-with(@id, 'post-')]")

		""" 处理回答 """
		if len(all_divs) > 0:
			for answer_item in all_divs:
				answer = Answer()
				answer.topic_id = topic_id

				if answer_item.xpath(".//div[@class='nick_name']/a[1]/@href"):
					author_info = answer_item.xpath(".//div[@class='nick_name']/a[1]/@href").extract()[0]
					author_id = author_info.split("/")[-1]
					answer.author_id = author_id
				if answer_item.xpath(".//label[@class='date_time']/text()"):
					create_time_str = answer_item.xpath(".//label[@class='date_time']/text()").extract()[0]
					create_time = datetime.strptime(create_time_str, "%Y-%m-%d %H:%M:%S")
					answer.create_time = create_time
				if answer_item.xpath(".//div[@class='post_body post_body_min_h']"):
					content = answer_item.xpath(".//div[@class='post_body post_body_min_h']").extract()[0]
					answer.content = content
				if answer_item.xpath(".//label[@class='red_praise digg']/em/text()"):
					praise_nums = answer_item.xpath(".//label[@class='red_praise digg']/em/text()").extract()[0]
					answer.praise_nums = int(praise_nums)

				self.answer_lock.acquire()
				answer.save()
				self.answer_lock.release()

		if sel.xpath("//a[contains(@class,'pageliststy next_page') and contains(text(), '下一页')]/@href"):
			next_page_href = \
			sel.xpath("//a[contains(@class,'pageliststy next_page') and contains(text(), '下一页')]/@href").extract()[0]
			next_page_url = parse.urljoin(self.http_prefix, next_page_href)
			# 解析下一页的回复
			self.parse_topic_of_next_page(next_page_url, topic_id)

	def parse_author(self, author_url):
		"""
		获取帖子的作者
		"""

		author_id = author_url.split("/")[-1]
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
		}
		response_text = requests.get(author_url, headers=headers).text
		sel = Selector(text=response_text)

		author = Author()
		author.id = author_id

		if sel.xpath("//p[@class='lt_title']/text()"):
			name_str = sel.xpath("//p[@class='lt_title']/text()").extract()[2].strip()
			author.name = name_str
		if sel.xpath("//div[@class='me_chanel_det_item access'][1]/span/text()"):
			topic_nums_str = sel.xpath("//div[@class='me_chanel_det_item access'][1]/span/text()").extract()[0]
			author.topic_nums = topic_nums_str.strip()
		if sel.xpath("//div[@class='me_chanel_det_item access'][2]/span/text()"):
			answer_nums_str = sel.xpath("//div[@class='me_chanel_det_item access'][2]/span/text()").extract()[0]
			author.answer_nums = answer_nums_str.strip()
		if sel.xpath("//div[@class='me_chanel_det_item access'][3]/span/text()"):
			answer_rate_str = sel.xpath("//div[@class='me_chanel_det_item access'][3]/span/text()").extract()[0]
			answer_rate = 0.0
			answer_rate_match = re.search("(\\d+)%", answer_rate_str.strip())
			if answer_rate_match:
				answer_rate = answer_rate_match.group(1)
			author.answer_rate = float(answer_rate)
		if sel.xpath("//div[@class='fans']/a/span/text()"):
			follower_nums_str = sel.xpath("//div[@class='fans']/a/span/text()").extract()[0]
			author.follower_nums = follower_nums_str.strip()
		if sel.xpath("//div[@class='att']/a/span/text()"):
			following_nums_str = sel.xpath("//div[@class='att']/a/span/text()").extract()[0]
			author.following_nums = following_nums_str.strip()

		""" 保存author """
		self.author_lock.acquire()
		has_exist_in_db = Author.select().where(Author.id == author_id)
		if has_exist_in_db:
			author.save()
		else:
			author.save(force_insert=True)
		self.author_lock.release()


if __name__ == '__main__':
	urls = add_other_category_url()
	# urls = ["https://bbs.csdn.net/forums/Moderator"]
	common_topic_lock = Lock()
	common_answer_lock = Lock()
	common_author_lock = Lock()

	t1 = CsdnSpiderTask(urls=urls, topic_lock=common_topic_lock, answer_lock=common_answer_lock, author_lock=common_author_lock)
	t2 = CsdnSpiderTask(urls=urls, topic_lock=common_topic_lock, answer_lock=common_answer_lock, author_lock=common_author_lock)
	t3 = CsdnSpiderTask(urls=urls, topic_lock=common_topic_lock, answer_lock=common_answer_lock, author_lock=common_author_lock)
	t4 = CsdnSpiderTask(urls=urls, topic_lock=common_topic_lock, answer_lock=common_answer_lock, author_lock=common_author_lock)
	t5 = CsdnSpiderTask(urls=urls, topic_lock=common_topic_lock, answer_lock=common_answer_lock, author_lock=common_author_lock)
	t6 = CsdnSpiderTask(urls=urls, topic_lock=common_topic_lock, answer_lock=common_answer_lock, author_lock=common_author_lock)
	t7 = CsdnSpiderTask(urls=urls, topic_lock=common_topic_lock, answer_lock=common_answer_lock, author_lock=common_author_lock)
	t8 = CsdnSpiderTask(urls=urls, topic_lock=common_topic_lock, answer_lock=common_answer_lock, author_lock=common_author_lock)

	t1.start()
	t2.start()
	t3.start()
	t4.start()
	t5.start()
	t6.start()
	t7.start()
	t8.start()

	t1.join()
	t2.join()
	t3.join()
	t4.join()
	t5.join()
	t6.join()
	t7.join()
	t8.join()

	print("OK")
