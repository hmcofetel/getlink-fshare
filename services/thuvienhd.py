import sys
sys.path.append("../")
from pathlib import Path
from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup as BS
import requests
from windows.image_frame import ImageFrame
import threading
from windows.gif_frame import GifFrame

BG_ITEMS = '#131413'
BG_MENU = '#1f2120'
BG_FRAME = '#1f2120'
import time

class ThuVienHD():
	def __init__(self, master):
		self.master = Toplevel(master)
		self.master.iconbitmap('logo.ico')
		self.master.title('ThuVienHD.com')
		self.master.configure(background=BG_ITEMS)
		self.contain_url = []
		self.page = 1
		self.main_url = 'https://thuvienhd.com/recent'
		self.frame_menu()
		self.frame_contain()
		self.frame_page()
		self.update_items(self.main_url)
		

		

	def frame_menu(self):
		frame_menu =  Frame(self.master, bg = BG_MENU)
		frame_menu.pack(side = TOP,fill = X)


		self.search_entry =  Entry(frame_menu, font = ('',13))
		self.search_entry.pack(side = RIGHT, fill = Y)
		self.search_entry.bind('<Return>', lambda e:threading.Thread(target =  self.update_items_search ).start())
		lb = Label(frame_menu,text = '🔎', font = ('', 15), bg = 'white')
		lb.pack(side = RIGHT, fill = Y)
		lb.config(width=3)
		self.title = Label(self.master,bg =BG_ITEMS,width = 50, fg = 'white',font = ('',30) ,text = 'RECENT')
		self.title.pack(side = TOP, fill = X)

		def button_click(text):
			self.set_main_url(text)
			threading.Thread(target = self.update_items , args = (self.main_url,)).start()  



		Button(frame_menu,bg = BG_ITEMS, bd =0 , highlightthickness=0, fg = 'white', font = ('', 15) ,text = 'Mới nhất', command = lambda: button_click('recent')).pack(side = LEFT)
		Button(frame_menu,bg = BG_ITEMS, bd =0 , highlightthickness=0, fg = 'white', font = ('', 15) , text = 'Hot', command = lambda: button_click('trending')).pack(side = LEFT)
		Button(frame_menu, bg = BG_ITEMS, bd =0 , highlightthickness=0, fg = 'white', font = ('', 15) ,text = 'h265', command = lambda: button_click('genre/h265')).pack(side = LEFT)
		Button(frame_menu, bg = BG_ITEMS,  bd =0 , highlightthickness=0,fg = 'white', font = ('', 15) ,text = 'TVB', command = lambda: button_click('genre/tvb')).pack(side = LEFT)
		Button(frame_menu, bg = BG_ITEMS,  bd =0 , highlightthickness=0,fg = 'white', font = ('', 15) ,text = 'Thuyết Minh', command = lambda: button_click('genre/thuyet-minh-tieng-viet')).pack(side = LEFT)
		Button(frame_menu, bg = BG_ITEMS,  bd =0 , highlightthickness=0,fg = 'white', font = ('', 15) ,text = 'Lồng Tiếng', command = lambda: button_click('genre/long-tieng-tieng-viet')).pack(side = LEFT)
	def set_main_url(self,url):
		self.main_url = 'https://thuvienhd.com/' + url
		self.title.config(text = url.upper())


	def _on_mousewheel(self, event):
		self.canvas_items.yview_scroll(int(-1*(event.delta/120)), "units")

	def frame_contain(self):
		self.frame_contain = Frame(self.master, bg = BG_ITEMS, highlightbackground=BG_FRAME, highlightthickness=10)
		self.frame_contain.pack(side  = TOP, fill = BOTH, expand = True, pady = 10, padx = 10)
		self.gif = GifFrame(self.frame_contain, path = 'images/loading.gif', bg = BG_ITEMS,  width = 1200, height = 500)
		self.gif.pack_forget()
	
		self.canvas_items = Canvas(self.frame_contain,bg = BG_ITEMS, highlightbackground=BG_ITEMS, highlightthickness=1, width = 1200, height = 500)
		self.canvas_items.pack(side = LEFT, fill =  BOTH , expand = True)

		self.canvas_items.bind_all("<MouseWheel>", self._on_mousewheel)



		style=ttk.Style()
		style.theme_use('default')
		style.configure("Vertical.TScrollbar",background="white", darkcolor=BG_ITEMS, lightcolor=BG_ITEMS,
                		troughcolor=BG_ITEMS, bordercolor=BG_ITEMS, arrowcolor=BG_ITEMS)
		
		self.scrollbar_canvas = ttk.Scrollbar(self.frame_contain , orient = VERTICAL, command =self.canvas_items.yview )
		self.scrollbar_canvas.pack(side = RIGHT, fill =Y)

		self.canvas_items.configure(yscrollcommand = self.scrollbar_canvas.set)
		self.canvas_items.bind('<Configure>', lambda e:self.canvas_items.configure(scrollregion =  self.canvas_items.bbox("all")))	
		self.frame_items()
		
	def frame_page(self):
		frame =  Frame(self.master, bg = BG_ITEMS)
		frame.pack(side = TOP)
		Button(frame, text = '<',bd =0 , fg = 'white', bg = BG_ITEMS,command = lambda:threading.Thread(target = self.prev_page ).start() ).pack(side = LEFT)
		self.lb_page =  Label(frame,  text= self.page, fg = 'white', bg = BG_ITEMS, font =('',14))
		self.lb_page.pack(side = LEFT, padx = 10)
		Button(frame, text = '>',bd =0, fg = 'white', bg = BG_ITEMS, command = lambda:threading.Thread(target = self.next_page ).start() ).pack(side = LEFT)

	def next_page(self):
		self.page += 1
		self.lb_page.config(text = self.page)
		self.clear_items()
		self.update_items(self.main_url + '/page/' + str(self.page))

	def prev_page(self):
		if  self.page > 1:
			self.page -= 1
			self.lb_page.config(text = self.page)
			self.clear_items()
			self.update_items(self.main_url + '/page/' + str(self.page))




	def frame_items(self):
		self.frame_items = Frame(self.canvas_items, bg = BG_ITEMS)
		self.canvas_items.create_window((0,0), window = self.frame_items, anchor = "nw")


	def get_items(self, url):
		self.items = []		
		page = requests.get(url)
		soup = BS(page.content,'html.parser')
		soup = soup.findAll("article",{"class":"item movies"})
		for data in soup:
			item = {
				'qualify':data.find("span",{"class":"quality_slider"}).text,
				'poster':data.img['src'],
				'kbd_quality':data.find("span",{"class":"kbd-quality"}).text if data.find("span",{"class":"kbd-quality"}) != None else ' ' ,
				'kbd_series':data.find("span",{"class":"kbd-series"}).text if data.find("span",{"class":"kbd-series"}) != None else ' ' ,
				'year':data.find("div",{"class":"data"}).span.text,
				'url':data.h3.a['href'],
				'name':data.h3.text.strip()
			}
			self.items.append(item)

	def search_items(self,q):
		
		self.items = []	
		page =  requests.get('https://thuvienhd.com/?s=' + q.replace(' ','+'))
		soup = BS(page.content,'html.parser')
		soup = soup.findAll("div",{"class":"result-item"})

		for data in soup:
			item = {
						'qualify':' ',
						'poster':data.find("div",{"class":"thumbnail animation-2"}).a.img['src'],
						'kbd_quality':' ' ,
						'kbd_series': ' ' ,
						'year':data.find("span",{"class":"year"}).text.strip(),
						'url':data.find("div",{"class":"thumbnail animation-2"}).a['href'],
						'name':data.find("div",{"class":"title"}).a.text
					}

			self.items.append(item)


	def conig_item(self, root_frame, index):
		try:
			img = ImageFrame(root_frame,bg = BG_ITEMS, url =  self.items[index]['poster'], command = lambda index = index: self.thread_get_contain_url(index) )
			img.pack()
			Label(img, text = self.items[index]['qualify'], bg= 'red', fg = 'white').place(x= 1, y = 1) if self.items[index]['qualify'] != ' ' else None
			Label(img, text = self.items[index]['kbd_quality'], bg= 'red', fg = 'white').place(x= 1, y = 25) if self.items[index]['kbd_quality'] != ' ' else None
			Label(img, text = self.items[index]['kbd_series'], bg= 'red', fg = 'white').place(x= 150, y = 1) if self.items[index]['kbd_series'] != ' ' else None
			Label(root_frame,width = 10, bg = BG_ITEMS, fg ='white',anchor = W, font = ('Roboto', 12) ,text = self.items[index]['name']).pack(fill = X)
			Label(root_frame,width = 10, bg = BG_ITEMS, fg ='white',anchor = W, font = ('Roboto', 10) ,text = self.items[index]['year']).pack(fill = X)
		except: pass	

	def get_contain_url(self, url):
		page =  requests.get(url)
		soup = BS(page.content,'html.parser')
		soup = soup.find("a",{"id":"download-button"})['href']
		page =  requests.get(soup)
		soup = BS(page.content,'html.parser')
		soup = [(item['href']) for item in  soup.findAll("a",{"class":"face-button"}) if 'fshare' in item['href'] ]
		self.contain_url = soup
		self.master.destroy()

	def thread_get_contain_url(self, index):
		self.canvas_items.pack_forget()
		self.gif.pack()
		threading.Thread(target = self.get_contain_url, args = (self.items[index]['url'],)).start()


	def thread_loading(self,command):
		t = threading.Thread(target = command)
		t.start()
		t.join()
		time.sleep(0.1)
		# ImageFrame(root, self.items[index]['poster'], command = lambda i= index:print(i)).pack(side = TOP, padx = 5, pady= 5)
		self.canvas_items.configure(scrollregion=self.canvas_items.bbox("all"))



	def thread_loading_items(self, url):
		self.get_items(url)
		index =  0
		for row in range(4):
			row_frame = Frame(self.frame_items,bg = BG_ITEMS)
			row_frame.pack(side = TOP)
			for column in range(5):
				column_frame = Frame(row_frame,bg = BG_ITEMS)
				column_frame.pack(side = LEFT,pady= 30, padx = 30)
				threading.Thread(target = self.thread_loading , args = (lambda index = index, column_frame = column_frame: self.conig_item(column_frame,index),) ).start()
				index += 1


	def thread_loading_search_items(self):
		self.search_items(self.search_entry.get())
		index =  0
		for row in range(4):
			row_frame = Frame(self.frame_items,bg = BG_ITEMS)
			row_frame.pack(side = TOP)
			for column in range(5):
				column_frame = Frame(row_frame,bg = BG_ITEMS)
				column_frame.pack(side = LEFT,pady= 30, padx = 30)
				threading.Thread(target = self.thread_loading , args = (lambda index = index, column_frame = column_frame: self.conig_item(column_frame,index),) ).start()
				index += 1


	
	def update_items(self,url):
		self.clear_items()
		self.canvas_items.pack_forget()
		self.gif.pack()
		t = threading.Thread(target = self.thread_loading_items, args =(url,))
		t.start()
		t.join()
		self.canvas_items.pack()
		self.gif.pack_forget()


	def update_items_search(self,):
		self.clear_items()
		self.canvas_items.pack_forget()
		self.gif.pack()
		t = threading.Thread(target = self.thread_loading_search_items)
		t.start()
		t.join()
		self.canvas_items.pack()
		self.gif.pack_forget()
		
		

				
	def clear_items(self):
		for widget in self.frame_items.winfo_children():
			threading.Thread(target = widget.destroy()).start()
			


	def show(self):
		self.master.deiconify()
		self.master.wait_window()
		return self.contain_url




def button_on():
	url = ThuVienHD(root).show()
	print(url)
	

if __name__ == '__main__':
	root = Tk()
	Button(root, text = 'Show', command = lambda:threading.Thread(target = button_on).start() ).pack()
	root.mainloop()


