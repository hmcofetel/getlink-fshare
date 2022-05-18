import requests
import json

class Fshare:
	def __init__(self, app_key,user_agent):
		self.app_key = app_key
		self.user_agent = user_agent
		self.BASE_URL = 'https://api.fshare.vn'

	def login(self, email, password):
		API_URL = '/api/user/login'
		data = '{"app_key":"%s","user_email":"%s","password":"%s"}' % (self.app_key, email, password)
		headers = {'cache-control': "no-cache", 'User-Agent': self.user_agent}
		result = requests.post(self.BASE_URL + API_URL, data = data, headers = headers)
		return result.json()

	def get_file_infor(self, url, token, session):
		API_URL = '/api/fileops/get'
		data   = '{"token" : "%s", "url" : "%s"}' % (token,url)
		header = {'User-Agent': self.user_agent,'Cookie' : 'session_id=' + session }
		result = requests.post(self.BASE_URL + API_URL,headers=header,data=data)
		return result.json()


	def get_link_download(self,url, token, session, password):
		API_URL = '/api/session/download'
		data   = '{"token" : "%s", "url" : "%s", "password" : "%s"}'% (token, url, password)
		header = {'Cookie' : 'session_id=' + session}
		result = requests.post(self.BASE_URL + API_URL, headers=header, data=data,verify=False)
		return result.json()

	def get_list_folder(self,url,token, session, page, limit):
		API_URL = '/api/fileops/getFolderList'
		data = '{"url": "%s","dirOnly": 0,"pageIndex": %s,"limit": "%s","token": "%s"}' % (url,str(page),str(limit),token)
		header = {'User-Agent': self.user_agent,'Cookie' : 'session_id=' + session }
		result = requests.post(self.BASE_URL + API_URL, headers=header, data=data)
		return result.json()

	def get_count_folder(self, url, token, session):
		API_URL = '/api/fileops/getTotalFileInFolder'
		data = '{"url": "%s","token": "%s","have_file": false}' % (url,token)
		header = {'User-Agent': self.user_agent,'Cookie' : 'session_id=' + session }
		result = requests.post(self.BASE_URL + API_URL, headers=header, data=data)
		return result.json()





