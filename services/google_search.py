import requests
class GoogleSearch:
	def __init__(self, key, cx):
		self.params = {
			'key':key,
			'cx':cx,
			'q':''
		}
		self.url_api = 'https://www.googleapis.com/customsearch/v1'

	def get_items_search(self, q):
		self.params['q'] = q
		page = requests.get(self.url_api, params = self.params)
		data = page.json()
		try:
			return [item['link'] for item in data['items'] ]
		except: return []

if __name__ == '__main__':
	app = GoogleSearch('AIzaSyC_4MhhBWREyn7S7qpQN348rRb6HH_Um_8','c7954a67903197864')
	search = app.get_items_search('conan')
