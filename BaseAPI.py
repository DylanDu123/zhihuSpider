#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib


def get_headers():
	# 构造 Request headers
	headers = {
		"Host": "www.zhihu.com",
		"Referer": "https://www.zhihu.com/",
		'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
	}
	return headers

def get_session():
	session = requests.session()
	# 使用登录cookie信息
	session.cookies = cookielib.LWPCookieJar(filename='cookies')
	try:
		session.cookies.load(ignore_discard=True)
	except:
	    print("Cookie 未能加载")		
	return session