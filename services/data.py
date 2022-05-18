import json
class Data:
	def load_data(self):
		try:
			data = {
				'email':'',
				'password':'',
				'token':'',
				'session':'',
				'timelog':''
			}
			json.dump(data,open('data.json','x') )
			
		except:
			data = json.load(open('data.json','r'))

		return data;

	def load_favorites(self):
		try:
			data = []
			json.dump(data,open('favorites.json','x') )
		except:
			data = json.load(open('favorites.json','r'))

		return data;	

	def save_data(self,data):
		json.dump(data, open('data.json','w'))

	def save_favorites(self,data):
		json.dump(data, open('favorites.json','w'))

	def get_size(self,size):
		size = float(size)
		
		if float(size) < 1024:
			return f'{size} Byte'

		elif float(size) < 1024**2:
			return f'{round(size/(1024),2)} KB' 

		elif float(size) < 1024**3:
			return f'{round(size/(1024**2),2)} MB'

		elif float(size) < 1024**4:
			return f'{round(size/(1024**3),2)} GB'


if __name__ == '__main__':
	
	load_favorites()