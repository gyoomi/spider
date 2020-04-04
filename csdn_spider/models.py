#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import *

db = MySQLDatabase("spider", host="127.0.0.1", port=3306, user="root", password="root")


class BaseModel(Model):
    class Meta:
        database = db


class Topic(BaseModel):
    # 主键，来自CSDN页面,非自增
    id = IntegerField(primary_key=True)
    # 标题
    title = CharField(max_length=500)
    # 内容
    content = TextField(default="")
    # 作者id
    author_id = CharField()
    # 创建时间
    create_time = DateTimeField()
    # 回答数量
    answer_nums = IntegerField(default=0)
    # 点击数
    click_nums = IntegerField(default=0)
    # 点赞数
    praise_nums = IntegerField(default=0)
    # 结帖率
    jtl = FloatField(default=0.0)
    # 悬赏分数
    score = IntegerField(default=0)
    # 状态： TODO
    status = CharField()


class Answer(BaseModel):
    # 主键：自增
    id = PrimaryKeyField()
    # 主题id
    topic_id = IntegerField()
    # 作者id
    author_id = CharField()
    # 回答内容
    content = TextField(default="")
    # 回答时间
    create_time = DateTimeField()
    # 点赞数
    praise_nums = IntegerField(default=0)


class Author(BaseModel):
    # 作者id: 来源CSDN页面标识
    id = CharField(primary_key=True)
    # 作者名称
    name = CharField()
    # 访问数
    click_nums = IntegerField(default=0)
    # 原创数
    original_nums = IntegerField(default=0)
    # 转发数
    forward_nums = IntegerField(default=0)
    # 排名数
    rate = IntegerField(default=0)
    # 评论数
    answer_nums = IntegerField(default=0)
    # 获赞数
    praise_nums = IntegerField(default=0)
    # 描述
    desc = TextField(null=True)
    # 行业
    industry = CharField(null=True)
    # 地理位置
    location = CharField(null=True)
    # 粉丝数
    follower_nums = IntegerField(default=0)
    # 关注数
    following_nums = IntegerField(default=0)


if __name__ == '__main__':
    db.create_tables([Topic, Answer, Author])
