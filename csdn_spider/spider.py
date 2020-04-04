#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import ast
from urllib import parse

import requests

from csdn_spider.models import *

# csdn解析到的所有的url
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


if __name__ == '__main__':
	# list1 = add_other_category_url()
	resp_text = requests.get("https://bbs.csdn.net/forums/ios").text
	print(resp_text)
