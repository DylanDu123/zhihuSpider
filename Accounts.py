#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import BaseAPI
import Login
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json

class Account(object):
	"""docstring for Account"""
	def __init__(self):
		super(Account, self).__init__()
		self.session = BaseAPI.get_session();
		self.get_userID()

	def get_userID(self):
		url = "https://www.zhihu.com/settings/profile"
		login_page = self.session.get(url, headers=BaseAPI.get_headers(), allow_redirects=False)
		html = login_page.text
		pattern = r'<a href="/people/(.*?)" class="zu-top-nav-userinfo ">'
		result = re.findall(pattern,html)
		self.userID = result[0]

	def insert_db(self,info):
		client = MongoClient()
		db = client.rpv
		account = db.account
		account.insert({info['uid']:info})

	def get_userInfo(self):
		print(self.userID)
		user_url = 'https://www.zhihu.com/people/' + self.userID
		user_page = self.session.get(user_url, headers = BaseAPI.get_headers(), allow_redirects=False)
		soup = BeautifulSoup(user_page.content ,'lxml')
		name = soup.find_all('span', {'class': 'name'})[1].string
		print(name)

		location = soup.find('span', {'class': 'location item'})
		if location == None:
			location = 'None'
		else:
			location = location.string
		print('居住地--' + location)

		business = soup.find('span', {'class': 'business item'})
		if business == None:
			business = 'None'
		else:
			business = business.string
		print('行业--' + business)

		gender = soup.find('input', {'checked': 'checked'})
		if gender == None:
			gender = 'None'
		else:
			gender = gender['class'][0]
		print('性别--' + gender)

		employment = soup.find('span', {'class': 'employment item'})
		if employment == None:
			employment = 'None'
		else:
			employment = employment.string
		print(employment)

		position = soup.find('span', {'class': 'position item'})
		if position == None:
			position = 'None'
		else:
			position = position.string
		print('公司名字--' + position)

		education = soup.find('span', {'class': 'education item'})
		if education == None:
			education = 'None'
		else:
			education = education.string
		print('学校--' + education)

		major = soup.find('span', {'class': 'education-extra item'})
		if major == None:
			major = 'None'
		else:
			major = major.string
		print('专业--' + major)

		temp = soup.find('img', {'alt': name})
		avatar_url = temp['src'][0:-6] + temp['src'][-4:]
		print('头像--' + avatar_url)

		agree = int(soup.find('span', {'class': 'zm-profile-header-user-agree'}).strong.string)
		print(agree)
		thanks = int(soup.find('span', {'class': 'zm-profile-header-user-thanks'}).strong.string)
		print(thanks)
		infolist = soup.find_all('a', {'class': 'item'})
		asks = int(infolist[1].span.string)
		print(asks)
		answers = int(infolist[2].span.string)
		print(answers)
		posts = int(infolist[3].span.string)
		print(posts)
		collections = int(infolist[4].span.string)
		print(collections)
		logs = int(infolist[5].span.string)
		print(logs)
		followees = int(infolist[len(infolist)-2].strong.string)
		print(followees)
		followers = int(infolist[len(infolist)-1].strong.string)
		print(followers)
		scantime = int(soup.find_all('span', {'class': 'zg-gray-normal'})[len(soup.find_all('span', {'class': 'zg-gray-normal'}))-1].strong.string)
		print(scantime)

		info = {
				'name':name,
				'uid':self.userID,
				'location':location,
				'business':business,
				'gender':gender,
				'employment':employment,
				'position':position,
				'education':education,
				'major':major,
				'agree':agree,
				'thanks':thanks,
				'asks':asks,
				'answers':answers,
				'posts':posts,
				'collections':collections,
				'logs':logs,
				'followers':followers,
				'followers':followers,
				'scantime':scantime
				}
		self.insert_db(info = info)
		return info

if __name__ == '__main__':
	lc = Login.Logincontrol()
	lc.login()
	ac = Account()
	ac.get_userInfo()