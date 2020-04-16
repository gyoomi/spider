#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import *

db = MySQLDatabase("spider", host="127.0.0.1", port=3306, user="root", password="root", charset="utf8mb4")


class BaseModel(Model):
    class Meta:
        database = db


