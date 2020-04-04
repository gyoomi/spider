#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import *
from datetime import date

db = MySQLDatabase("spider", host="127.0.0.1", port=3306, user="root", password="root")


class Person(Model):
	id = PrimaryKeyField(column_name="uid")
	name = CharField(null=True, max_length=100)
	birthday = DateField(null=True)

	class Meta:
		database = db  # This model uses the "people.db" database.
		table_name = "user"


# if __name__ == "__main__":
# 	db.create_tables([Person])
# 	print("init [OK]")

if __name__ == '__main__':

	# 新增
	# p = Person(name="jerry", birthday=date(1999, 2, 20))
	# p.save()

	# 查询
	# 查询单个
	# personInDb = Person.get_by_id(2)
	# print(personInDb.name + ", " + str(personInDb.birthday))
	# p = Person.select().where(Person.name == "tom").get()
	# print(p.name + ", " + str(p.birthday))
	# 查询列表
	# personList = Person.select().where(Person.name == "jerry")
	# for p in personList:
	# 	print(p.name + ", " + str(p.birthday))

	# 删除
	# personList = Person.select().where(Person.name == "jerry")
	# for p in personList:
	# 	p.delete_instance()

	print("ok")
