#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import os.path
try:
    from PIL import Image
except:
    pass
import BaseAPI
		
class Logincontrol(object):
	"""docstring for LoginControl"""
	def __init__(self):
		super(Logincontrol, self).__init__()
		self.session = BaseAPI.get_session();

	def isLogin(self):
	    # 通过查看用户个人信息来判断是否已经登录
	    url = "https://www.zhihu.com/settings/profile"
	    login_page = self.session.get(url, headers=BaseAPI.get_headers(), allow_redirects=False)
	    login_code = login_page.status_code
	    if login_code == 200:
	        return True
	    else:
	        return False

	def get_xsrf(self,url):
	 	index_url = url
	 	index_page = self.session.get(index_url,headers=BaseAPI.get_headers())
	 	html = index_page.text
	 	pattern = r'name="_xsrf" value="(.*?)"'
	 	_xsrf = re.findall(pattern,html)
	 	return _xsrf[0]

	def get_captcha(self):
		t = str(int(time.time() * 1000))
		captcha_url = "http://www.zhihu.com/captcha.gif?r=" + t + "&type=login"
		r = self.session.get(captcha_url,headers=BaseAPI.get_headers())
		with open("captcha.jpg","wb") as f:
			f.write(r.content)
			f.close()
		try:
			im = Image.open("captcha.jpg")
			im.show()
			im.close()
		except:
			print*(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
		captcha = input("please input the captcha\n")
		return captcha
    
	def login(self):
		if self.isLogin():
			print('您已登录')
		else:
			account = input('请输入用户名\n')
			pwd = input('请输入密码\n')
			if re.match(r"^1\d{10}$",account):
				print('手机号登录')
				post_url = 'http://www.zhihu.com/login/phone_num'
				postdata = {
					'_xsrf':self.get_xsrf("http://www.zhihu.com"),
					"password":pwd,
					"remember_me":"true",
					"phone_num":account
				}
			else:
				if "@" in account:
					print('邮箱登录')
				else:
					print('输入账号有问题')
					return 0
				post_url = 'http://www.zhihu.com/login/email' 
				postdata = {
					'_xsrf': self.get_xsrf("http://www.zhihu.com"),
					"password":pwd,
					"remember_me":"true",
					"email":account
				}
			try:
				login_page = session.session.post(post_url,date=postdata,headers=BaseAPI.get_headers())
				print(login_page.text)
			except:
				postdata["captcha"] = self.get_captcha()
				login_page = self.session.post(post_url,data=postdata,headers=BaseAPI.get_headers())
				login_code = eval(login_page.text)
				print(login_code["msg"])
			self.session.cookies.save()



if __name__ == '__main__':
	lc = Logincontrol()
	lc.login()