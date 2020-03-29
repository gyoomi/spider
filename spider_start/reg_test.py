#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

info = "姓名：张三 生日： 1998-10-10 本科： 2019-09-01"

'''
1. 提取字符串
2. 替换
3. 搜索
'''

# 1
# match_result = re.match(".*生日.*?(\d{4}).*本科.*?(\d{4})", info)
# print(match_result.group(0))
# print(match_result.group(1))
# print(match_result.group(2))

# 2
# sub_result = re.sub("\d{4}", "2020", info)
# print(info)
# print(sub_result)

# 3
# match_result = re.search("生日.*?(\d{4}).*本科.*?(\d{4})", info)
# print(match_result.group(1))
# print(match_result.group(2))

stu = """my name is
	  张三
	  """

print(re.search("张三", stu).group())
print(re.match(".*(张三)", stu, re.DOTALL).group(1))
