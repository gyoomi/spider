#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title12313123</title>
</head>
<body>
	<table border="1">
		<tr>
			<th>人物</th>
			<th>介绍</th>
			<th>产品</th>
		</tr>
		<tr>
			<td>史蒂夫·保罗·乔布斯</td>
			<td>苹果CEO</td>
			<td>Apple系列</td>
		</tr>
		<tr>
			<td>丹尼斯·里奇</td>
			<td>C语言之父</td>
			<td>C语言</td>
		</tr>
		<tr>
			<td>比尔·盖茨</td>
			<td>微软CEO</td>
			<td>Windows系统</td>
		</tr>
	</table>
		<div id="container">
			<div>
				哈哈哈，则是div的内容
			</div>
			<div name="testDiv" id="test" class="follow-11 h01" data="111 222 哈哈">
				哈哈哈哈
			</div>
	</div>
</body>
</html>
"""

bs = BeautifulSoup(html, "html.parser")
# title_tag = bs.title
# print(title_tag)
# print(title_tag.string)

# div_tag = bs.div
# print(div_tag)

# div_tags = bs.find("div")
# print(div_tags)
# for tag in div_tags:
# 	print(tag)

# div_tags = bs.find_all("div")
# for tag in div_tags:
# 	print(tag)

# div_tag = bs.find(id="container")
# print(div_tag)

# div_tag = bs.find("div", id="test")
# print(div_tag)

# div_tag = bs.find("div", {"name": "testDiv"})
# print(div_tag)

# sibling_tags = bs.find("div", {"name": "testDiv"}).previous_siblings
# for tag in sibling_tags:
# 	print(tag)
# 	print("---")


div_tag = bs.find("div", {"name": "testDiv"})
print(div_tag["class"])
print(div_tag.get("class"))
print(div_tag.get("data"))
print(div_tag["data"])