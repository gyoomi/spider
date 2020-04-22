#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import *

db = MySQLDatabase("spider", host="127.0.0.1", port=3306, user="root", password="root", charset="utf8mb4")


class BaseModel(Model):
    class Meta:
        database = db


class Good(BaseModel):
    """
        商品对象
    """
    id = BigIntegerField(primary_key=True, verbose_name="主键")
    name = CharField(max_length=500, verbose_name="商品名")
    price = FloatField(default=0.0, verbose_name="商品价格")
    content = TextField(default="", verbose_name="內容")
    supplier = CharField(max_length=500, verbose_name="供货商")
    ggbz = TextField(default="", verbose_name="规格和包装")
    image_list = TextField(default="")
    comment_nums = IntegerField(default=0, verbose_name="评论数")
    good_rate = IntegerField(default=0, verbose_name="好评率")
    has_image_comment_nums = IntegerField(default=0, verbose_name="晒图数")
    has_video_comment_nums = IntegerField(default=0, verbose_name="视频晒单数")
    has_add_comment_nums = IntegerField(default=0, verbose_name="追评数")
    good_comment_nums = IntegerField(default=0, verbose_name="好评数")
    middle_comment_nums = IntegerField(default=0, verbose_name="中评数")
    bad_comment_nums = IntegerField(default=0, verbose_name="差评数")


class GoodEvaluate(BaseModel):
    """
        商品的评论
    """
    id = CharField(primary_key=True, verbose_name="主键")
    good = ForeignKeyField(Good, verbose_name="商品主键")
    user_head_url = CharField(max_length=500, verbose_name="用户头像")
    user_name = CharField(verbose_name="用户名")
    good_info = CharField(max_length=500, verbose_name="购买时商品的信息")
    evaluate_time = DateTimeField(verbose_name="评价时间")
    content = TextField(default="", verbose_name="评论内容")
    star = IntegerField(default=0, verbose_name="评分")
    comment_nums = IntegerField(default=0, verbose_name="评论数")
    praised_num = IntegerField(default=0, verbose_name="点赞数")
    image_list = TextField(verbose_name="图片列表")
    video_list = TextField(verbose_name="视频列表")


class GoodEvaluateSummary(BaseModel):
    """
        商品评论标签汇总
    """
    good = ForeignKeyField(Good, verbose_name="商品")
    tag = CharField(max_length=100, verbose_name="标签")
    num = IntegerField(default=0, verbose_name="数量")


if __name__ == '__main__':
    db.create_tables([Good, GoodEvaluate, GoodEvaluateSummary])
    print("table init [OK]")
