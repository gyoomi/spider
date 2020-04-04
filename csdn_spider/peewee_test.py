#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import *

db = MySQLDatabase("spider", host="127.0.0.1", port=3306, user="root", password="root")


class Person(Model):
	id = PrimaryKeyField(column_name="uid")
	name = CharField(null=True, max_length=100)
	birthday = DateField(null=True)

	class Meta:
		database = db  # This model uses the "people.db" database.
		table_name = "user"


if __name__ == "__main__":
	db.create_tables([Person])
	print("init [OK]")
