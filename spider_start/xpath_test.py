#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scrapy import Selector

html = """
<html>
    <body>
        <h1>Hello World</h1>
        <h1>Hello Scrapy</h1>
        <h1>Hello python</h1>
        <ul>
            <li>C++</li>
            <li>java</li>
            <li>python</li>
        </ul>
    </body>
    <h1>哈哈哈</h1>
</html>
"""

selector = Selector(text=html)

# 选中内容中的所有h1标签
# data = selector.xpath("//h1")
# print(data)

data = selector.xpath("body/h1[4]")
print(data)


