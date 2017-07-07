#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
import urllib
import requests
import cookielib
import json
import logging
import zlib
import time

logging.basicConfig(level=logging.DEBUG)
reload(sys)
sys.setdefaultencoding("utf8")

true = 1
false = 0

class SMZDM(object):
 
	def __init__(self,name,password,is_sigin):
		self.name = name;
		self.password = password;
		self.is_signin = is_sigin;
		self.cj = cookielib.LWPCookieJar();
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj));
		urllib2.install_opener(self.opener);
	 
	def _getHeaders(self):
		headers = {
			'Accept':'application/json, text/javascript, */*; q=0.01',
			'Accept-Encoding':'gzip, deflate, br',
			'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
			'Connection':'keep-alive',
			'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			'Host':'zhiyou.smzdm.com',
			'Origin':'https://zhiyou.smzdm.com',
			'Referer':'https://zhiyou.smzdm.com/user/login',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'X-Requested-With':'XMLHttpRequest'
		} 
		return headers

	def _getSigninHeaders(self):
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
		}
		return headers
	 
	def login(self):
		'''登录网站'''
 #	   logging.debug(u'正在登陆 username : %s password : %s' %(self.name,self.password))
 #	   logging.debug(u'\nheaders is : %s' % self._getHeaders())
		loginparams = {'username': self.name,'password':self.password,'remember':'0','captcha':'0'}
 #	   logging.debug(u'\nloginparams is : %s' % loginparams)
		req = urllib2.Request( r'https://zhiyou.smzdm.com/user/login/ajax_check', urllib.urlencode(loginparams), headers=self._getHeaders())
		response = urllib2.urlopen(req)

		content = response.read()

		content = zlib.decompress(content, 16+zlib.MAX_WBITS)  # decompress since 'Accept-Encoding':'gzip, deflate, br' in headers

		params = json.loads(content);

		if(params['error_code'] == 0):
			print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() )) ) +' '+self.name+u'登陆成功.\n'
			return true
		else:
			print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() )) )+' '+self.name+u'登录失败.' + params['error_msg'];
			return false

		return false
			 
	def sign(self):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:20.0) Gecko/20100101 Firefox/20.0',
			'Host': 'zhiyou.smzdm.com',
			'Referer': 'http://www.smzdm.com/'
		}
#		logging.debug( 'start sign\n')
		req = urllib2.Request(r'http://www.smzdm.com/user/checkin/jsonp_checkin', headers=headers)
		try:
			response = urllib2.urlopen(req)
			content = response.read()
			params = json.loads(content)
			if(params['error_code'] == 0):
				print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() )) )+' '+self.name+u'签到成功.\n'
				return true;
			else:
				print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() )) ) +' '+self.name+u'签到失败.' + params['error_msg'];
				return false;
		except Exception as e:
			print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() )) )+' '+self.name+u'异常！签到失败: ',e
			return false;


	 
if __name__ == '__main__':
	userlogin = [SMZDM('usr1','pwd1',false),SMZDM('usr2','pwd2',false)];
	while(True):
		current_time = time.localtime(time.time())
		if(current_time.tm_hour == 0):
			print(str( time.strftime('%Y-%m-%d %H:%M:%S',current_time) )+u' 新的一天开始了.\n');
			
		for usr in userlogin:
			if(time.strftime('%Y-%m-%d',current_time) == last_signin_date):
				usr.is_signin = true;
			else:
				usr.is_signin = false;
		
			if(usr.is_signin == false):
				if(usr.login() == true):
					if(usr.sign() == true):
						usr.is_signin = true;
				
		last_signin_date = time.strftime('%Y-%m-%d',current_time);				
#		print(str( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() )) )+u' 休眠1小时');
		
		time.sleep(3600);