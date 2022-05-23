import cloudscraper
from tkinter import *
from bs4 import BeautifulSoup as BS
import threading
from windows.gif_frame import GifFrame
import os
import pathlib

from zipfile import ZipFile

class Subscene():
	def __init__(self, master):
		self.master = Toplevel(master)
		self.items =  []
		self.subs = []
		self.path_sub = ''
		self.state = 0
		self.web = 'https://subscene.com'

		self.frame_menu()
		self.frame_listbox()




	def thread_click(self, *args):
		threading.Thread(target = self.thread_loading, args = args).start()



	def thread_loading(self, command, *args):
		self.frame_listbox.pack_forget()
		self.loading_gif.pack(expand = True, fill = BOTH)
		t = threading.Thread(target = command, args = args)
		t.start()
		t.join()
		self.frame_listbox.pack(expand = True, fill = BOTH)
		self.loading_gif.pack_forget()


		


	def frame_menu(self):
		frame_menu = Frame(self.master)
		frame_menu.pack(side = TOP, fill = X)
		self.q_entry =  Entry(frame_menu)
		self.q_entry.pack(side = TOP,anchor = W)
		self.q_entry.bind('<Return>',lambda e:self.thread_click(self.search_sub, self.q_entry.get()) )
		Button(frame_menu, text  = 'Downloaded Subs', command = lambda:self.thread_click(self.list_download)).pack(side = TOP, anchor =  W)

	def list_download(self):
		self.state =3
		self.extract_sub =[]
		for data in  os.listdir('./services/download/extract'):
			item = {
				'name':data,
				'path':str(pathlib.Path(__file__).parent.joinpath('download/extract').joinpath(data)),
			}

			self.extract_sub.append(item)
		self.insert_listbox(self.extract_sub)

	def frame_listbox(self):
		frame_content = Frame(self.master)
		frame_content.pack(side = TOP, fill = BOTH, expand = True)

		self.frame_listbox =  Frame(frame_content)
		self.frame_listbox.pack(side = TOP, fill = BOTH,expand = True)

		self.loading_gif = GifFrame(frame_content, 'images/loading.gif')
		self.loading_gif.pack_forget()

		self.listbox  = Listbox(self.frame_listbox)
		self.listbox.pack(side = LEFT, fill = BOTH,expand = True)
		self.listbox.bind('<Double-Button-1>', lambda e : self.handle_dbclick())

		

		self.scrollbar = Scrollbar(self.frame_listbox)
		self.scrollbar.pack(side = RIGHT,fill = Y )

		self.listbox.config(yscrollcommand = self.scrollbar.set)
		self.scrollbar.config(command = self.listbox.yview)


	def insert_listbox(self, items):
		self.listbox.delete(0, END)
		for item in items:
			text = ''
			for element in item:
				text += '   |    '+ element + ': ' + item[element] 
				
			self.listbox.insert(END, text)


	def handle_dbclick(self):
		if self.state == 0:
			choose = self.listbox.curselection()[0]
			args = lambda:[self.get_list_subs(self.items[choose]['href']), self.insert_listbox(self.list_subs)]
			self.thread_click(args)
			self.state = 1
		elif self.state == 1:
			choose = self.listbox.curselection()[0]
			args = lambda:[self.download_subs(self.list_subs[choose]['href']), self.insert_listbox(self.extract_sub)]
			self.thread_click(args)
			self.state = 2

		elif self.state == 2:
			choose = self.listbox.curselection()[0]
			path_zip = pathlib.Path(__file__).parent.joinpath('download/temp.zip')
			zip_file  = ZipFile(path_zip, 'r')
			zip_file.extract(self.extract_sub[choose]['name'], pathlib.Path(__file__).parent.joinpath('download/extract'))
			self.path_sub = self.extract_sub[choose]['path']
			self.master.destroy()

		elif self.state == 3:
			choose = self.listbox.curselection()[0]
			self.path_sub = self.extract_sub[choose]['path']
			self.master.destroy()

			




	def search_sub(self, q):
		self.state = 0
		data = {
			'query': q,
			'l':''
		}
		self.items = []
		scraper = cloudscraper.create_scraper() 
		page = scraper.post('https://subscene.com/subtitles/searchbytitle', data = data)
		soup = BS(page.content,'html.parser')
		soup =  soup.findAll("div",{"class":"search-result"})
		soup = soup[0].ul.findAll('li')
		for data in soup:
			item = {
				'name':data.find('div',{'class':'title'}).a.text,
				'href':data.find('div',{'class':'title'}).a['href'],
				'cont':data.find('div',{'class':'subtle count'}).text.strip()
			}
			self.items.append(item)

		

		self.insert_listbox(self.items)

	def get_list_subs(self,href):
		scraper = cloudscraper.create_scraper() 
		page =  scraper.get(self.web+ href)
		soup = BS(page.content, 'html.parser') 
		soup = soup.findAll('td',{'class':'a1'})
		self.list_subs = []
		for data in soup:
			item  = {
				'href':data.a['href'],
				'lang':data.a.findAll('span')[0].text.strip(),
				'name':data.a.findAll('span')[1].text.strip()
			}
			self.list_subs.append(item)

	def download_subs(self, href):
		scraper = cloudscraper.create_scraper() 
		page =  scraper.get(self.web+href)
		soup = BS(page.content, 'html.parser') 
		soup = soup.find('div',{'class','download'})
		zip_sub =  scraper.get(self.web  + soup.a['href'],allow_redirects=True )
		open(pathlib.Path(__file__).parent.joinpath('download/temp.zip'), 'wb').write(zip_sub.content)
		self.extract_sub = []
		zip_file  = ZipFile(pathlib.Path(__file__).parent.joinpath('download/temp.zip'), 'r')
		data = zip_file.infolist()
		for info in data:
			item = {
				'name':info.filename,
				'path':str(pathlib.Path(__file__).parent.joinpath('download/extract').joinpath(info.filename)),
			}
			self.extract_sub.append(item)





	def show(self):
		self.master.deiconify()
		self.master.wait_window()
		return self.path_sub



if __name__ == '__main__':
	root = Tk()
	app = Subscene(root)
	root.mainloop()
	# app = Subscene()
	# app.search('iron man')
	# app.get_subs(app.items[0]['href'])
	# print(app.subs[0]['href'])
	# app.download_subs(app.subs[0]['href'])



		