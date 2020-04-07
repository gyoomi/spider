#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import *

db = MySQLDatabase("spider", host="127.0.0.1", port=3306, user="root", password="root", charset="utf8mb4")


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
    # 创建时间
    create_time = DateTimeField()
    # 最后回复时间
    last_answer_time = DateTimeField()


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
    name = CharField(default="")
    # 发帖数
    topic_nums = CharField(max_length=50, default="")
    # 回帖数
    answer_nums = CharField(max_length=50, default="")
    # 回帖率
    answer_rate = CharField(max_length=50, default="")
    # 粉丝数
    follower_nums = CharField(max_length=50, default="")
    # 关注数
    following_nums = CharField(max_length=50, default="")


if __name__ == '__main__':
    db.create_tables([Topic, Answer, Author])
    print("tables init [OK]")


