#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import BaseAPI
from Login import Logincontrol
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json
import time
import json

class Account(object):
	"""docstring for Account"""
	def __init__(self):
		super(Account, self).__init__()
		self.session = BaseAPI.get_session();

	def get_current_userInfo(self):
		url = "https://www.zhihu.com/settings/profile"
		login_page = self.session.get(url, headers=BaseAPI.get_headers(), allow_redirects=False)
		html = login_page.text
		print(login_page);
		pattern = r'<a href="(.*?)" class="zu-top-nav-userinfo ">'
		result = re.findall(pattern,html)

		soup = BeautifulSoup(html ,'lxml')
		title = soup.find('script', {'data-name': 'ga_vars','class':'json-inline'})
		user_info = json.loads(title.contents[0])
		user_info["user_address"] =  result[0]
		return user_info

	def get_user_deatailinfo(self,user_address):
		user_url = 'https://www.zhihu.com' + user_address
		userID = user_address[8:]
		user_page = self.session.get(user_url, headers = BaseAPI.get_headers(), allow_redirects=False)
		soup = BeautifulSoup(user_page.content ,'lxml')
		name = soup.find_all('span', {'class': 'name'})[1].string
		location = soup.find('span', {'class': 'location item'})
		if location == None:
			location = 'None'
		else:
			location = location.string
		business = soup.find('span', {'class': 'business item'})
		if business == None:
			business = 'None'
		else:
			business = business.string

		gender = soup.find('input', {'checked': 'checked'})
		if gender == None:
			gender = 'None'
		else:
			gender = gender['class'][0]

		employment = soup.find('span', {'class': 'employment item'})
		if employment == None:
			employment = 'None'
		else:
			employment = employment.string

		position = soup.find('span', {'class': 'position item'})
		if position == None:
			position = 'None'
		else:
			position = position.string

		education = soup.find('span', {'class': 'education item'})
		if education == None:
			education = 'None'
		else:
			education = education.string

		major = soup.find('span', {'class': 'education-extra item'})
		if major == None:
			major = 'None'
		else:
			major = major.string
		temp = soup.find('img', {'alt': name})
		avatar_url = temp['src'][0:-6] + temp['src'][-4:]
		agree = int(soup.find('span', {'class': 'zm-profile-header-user-agree'}).strong.string)
		thanks = int(soup.find('span', {'class': 'zm-profile-header-user-thanks'}).strong.string)
		infolist = soup.find_all('a', {'class': 'item'})
		asks = int(infolist[1].span.string)

		answers = int(infolist[2].span.string)
		posts = int(infolist[3].span.string)
		try:
			collections = ""
			collections = int(infolist[4].span.string)
		except:
			print(infolist)
		try:
			logs = ""
			logs = int(infolist[5].span.string)
		except:
			print(infolist)
		
		followees = int(infolist[len(infolist)-2].strong.string)
		followers = int(infolist[len(infolist)-1].strong.string)
		scantime = int(soup.find_all('span', {'class': 'zg-gray-normal'})[len(soup.find_all('span', {'class': 'zg-gray-normal'}))-1].strong.string)

		info = {
				'name':name,
				'uid':userID,
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
				'scantime':scantime,
				}
		user_info.update(info)
		return info

	def get_followees(self,user_address):
		followees_url = "https://www.zhihu.com" + user_address +"/followees"
		user_page = self.session.get(followees_url, headers = BaseAPI.get_headers(), allow_redirects=False)
		soup = BeautifulSoup(user_page.content, "lxml")
		follist = soup.select('div[class*="zm-profile-card"]')
		fol_user_addresses = []

		for followees in follist:
			tag = followees.a["href"]
			fol_user_addresses.append(tag)
		return fol_user_addresses;

	def set_info(self,user_infos):
		array = []
		for user_info in user_infos:
			followees =  user_info["followees"]
			person.update({'uid':user_info['uid']},user_info,True)
			for followees_address in followees:
				user_deatailinfo = self.get_user_deatailinfo(followees_address)
				followees =  self.get_followees(followees_address)
				user_deatailinfo["followees"] = followees
				array.append(user_deatailinfo)
				print(user_deatailinfo)
				person.update({'uid':user_deatailinfo['uid']},user_deatailinfo,True)
				time.sleep(2)
		self.set_info(array)
		

if __name__ == '__main__':
	lc = Logincontrol()
	lc.login()
	global person
	person = MongoClient().rpv.person
	ac = Account()
	user_info = ac.get_current_userInfo() 
	user_deatailinfo = ac.get_user_deatailinfo(user_info["user_address"])
	user_deatailinfo.update(user_info)
	followees =  ac.get_followees(user_info["user_address"])
	user_deatailinfo["followees"] = followees

	array = []
	array.append(user_deatailinfo)
	ac.set_info(array)
	# person.update({'uid':user_address[8:]},{"$pushAll":{"followees":fol_userids}})






