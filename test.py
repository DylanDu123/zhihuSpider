from pymongo import MongoClient

person = MongoClient().rpv.person
items = person.find()
for ite in items:
	print(type(ite))