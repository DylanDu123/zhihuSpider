from django.shortcuts import render_to_response
from django.http import HttpResponse
from pymongo import MongoClient
# Create your views here.


def index(req):
	person = MongoClient().rpv.person
	items = person.find()
	array = []
	for ite in items:
		array.append(ite)

	rs = render_to_response('index.html',{"title":"这的网页","item":array})
	return rs