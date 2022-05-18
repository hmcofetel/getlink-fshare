import sys
sys.path.append('../')
sys.path.append('../services')
from tkinter import *
import tkinter.messagebox as tkmsg 
from windows.giff_frame import GifFrame
from services.client import Client
from services.play_vlc import PLayVLC
import threading
import pyperclip

class MainWindow(Client, PLayVLC):
	def __init__ (self, master):
		super().__init__()
		self.master = master
		self.master.title('Fshare Getlink Tool')
		self.buffer = []
		self.buffer_index = -1
		self.win()

	def save_buffer(self):
		del self.buffer[self.buffer_index+1:]
		buffer = {
			'input_link':self.input_link.get(),
			'name_main_folder': self.name_main_folder.get(),
			'url_download':self.url_download.get(),
			'count_folder':self.count_folder.get(),
			'page_folder':self.page_folder.get(),
			'url_item':self.url_item.get(),
			'listbox':self.items
		} 
		self.buffer.append(buffer)
		self.buffer_index +=1
	
	def get_buffer(self):
		self.input_link.delete(0,END)
		self.name_main_folder.delete(0,END)
		self.url_download.delete(0,END)
		self.count_folder.delete(0,END)
		self.page_folder.delete(0,END)
		self.url_item.delete(0,END)
		self.listbox_name.delete(0,END)
		self.listbox_size.delete(0,END)
		self.listbox_file_type.delete(0,END)

		self.input_link.insert(END, self.buffer[self.buffer_index]['input_link'])
		self.name_main_folder.insert(END, self.buffer[self.buffer_index]['name_main_folder'])
		self.url_download.insert(END, self.buffer[self.buffer_index]['url_download'])
		self.count_folder.insert(END, self.buffer[self.buffer_index]['count_folder'])
		self.page_folder.insert(END, self.buffer[self.buffer_index]['page_folder'])
		self.url_item.insert(END, self.buffer[self.buffer_index]['url_item'])
		self.items = self.buffer[self.buffer_index]['listbox']
		for item in self.items :
			self.insert_item_listbox(item)

	def prev_buffer(self):
		if self.buffer_index > 0:
			self.buffer_index -= 1 
			self.get_buffer()

	def next_buffer(self):
		if self.buffer_index + 1 < len(self.buffer): 
			self.buffer_index += 1
			self.get_buffer()



	def run_thearding(self):
		url = self.input_link.get().split('/')
		if 'www.fshare.vn' in url and 'folder' in url:
			self.is_folder()


		elif 'www.fshare.vn' in url and 'file' in url:
			self.is_file()


		else:
			print('Wrong url')
			tkmsg.showerror(message = 'Wrong url !', title = 'Error')

		

	def handle_threading(self):
		self.listbox_frame.pack_forget()
		self.giff_frame.pack(fill = BOTH, expand = True)

		t = threading.Thread(target = self.run_thearding)
		t.start()
		t.join()

		self.giff_frame.pack_forget()
		self.listbox_frame.pack(fill =BOTH, expand = True)
		self.save_buffer()

	def check_url(self):

		threading.Thread(target = self.handle_threading).start()



		

	def get_link_item(self):
		data = self.load_data()
		result = self.get_link_download(self.url_item.get(), data['token'], data['session'], data['password'])
		if 'msg' in result:
			tkmsg.showerror(message = result['msg'])
		else:
			self.url_download.delete(0,END)
			self.url_download.insert(END, result['location'])

	def is_folder(self):
		
		self.url_item.delete(0,END)
		self.url_item.insert(END, self.input_link.get())
		data = self.load_data()
		self.name_main_folder.delete(0, END)
		self.name_main_folder.insert(END, self.get_file_infor(self.input_link.get(),data['token'], data['session'])['name'])
		self.items = self.get_list_folder(self.input_link.get(),data['token'], data['session'], int(self.page_folder.get()), int(self.items_per_pages.get()))
		self.listbox_name.delete(0,END)
		self.listbox_size.delete(0,END)
		self.listbox_file_type.delete(0,END)
		self.count_folder.delete(0,END)
		self.count_folder.insert(END, self.get_count_folder(self.input_link.get(),data['token'],data['session'])['total'])
		for item in self.items:
			self.insert_item_listbox(item)
			
	def is_file(self):
		self.name_main_folder.delete(0, END)
		self.url_item.delete(0,END)
		self.url_item.insert(END, self.input_link.get())
		data = self.load_data()
		self.items = [self.get_file_infor(self.input_link.get(),data['token'], data['session'])]
		self.listbox_name.delete(0,END)
		self.listbox_size.delete(0,END)
		self.listbox_file_type.delete(0,END)
		self.count_folder.delete(0,END)
		self.insert_listbox()


	def insert_listbox(self):
		for item in self.items:
			self.insert_item_listbox(item)


	def insert_item_listbox(self, item):
		if item['file_type'] == '1':
			self.listbox_name.insert(END,item['name'])
			self.listbox_name.itemconfigure(END,{'selectbackground':'cyan'})
			self.listbox_name.insert(END,'―'*300)
			self.listbox_name.itemconfigure(END,{'selectbackground':'white'})

			self.listbox_size.insert(END,self.get_size(item['size']) )
			self.listbox_size.itemconfigure(END,{'selectbackground':'white'})
			self.listbox_size.insert(END,'―'*300)
			self.listbox_size.itemconfigure(END,{'selectbackground':'white'})

			self.listbox_file_type.insert(END,item['mimetype'])
			self.listbox_file_type.itemconfigure(END,{'selectbackground':'white'})
			self.listbox_file_type.insert(END,'―'*300)
			self.listbox_file_type.itemconfigure(END,{'selectbackground':'white'})

		else:
			self.listbox_name.insert(END,item['name'])
			self.listbox_name.itemconfigure(END,{'bg':'yellow','selectbackground':'cyan'})
			self.listbox_name.insert(END,'―'*300)
			self.listbox_name.itemconfigure(END,{'bg':'yellow','selectbackground':'yellow'})

			self.listbox_size.insert(END,'NULL' )
			self.listbox_size.itemconfigure(END,{'bg':'yellow','selectbackground':'yellow'})
			self.listbox_size.insert(END,'―'*300)
			self.listbox_size.itemconfigure(END,{'bg':'yellow','selectbackground':'yellow'})

			self.listbox_file_type.insert(END,'Folder')
			self.listbox_file_type.itemconfigure(END,{'bg':'yellow','selectbackground':'yellow'})
			self.listbox_file_type.insert(END,'―'*300)
			self.listbox_file_type.itemconfigure(END,{'bg':'yellow','selectbackground':'yellow'})

	def handles_click_item(self, self_1):
		curselection = self.listbox_name.curselection()
		try:
			if int(curselection[0])%2 == 0 :
				self.url_item.delete(0,END)
				self.url_item.insert(END, self.items[int(curselection[0]/2)]['furl'])
		except: pass
 
	def handle_dbclick_item(self,self_1):
		curselection = self.listbox_name.curselection()
		try:
			if int(curselection[0])%2 == 0 and self.items[int(curselection[0]/2)]['file_type'] == '0':
				self.input_link.delete(0,END)
				self.input_link.insert(END, self.items[int(curselection[0]/2)]['furl'])
				self.check_url()

		except:pass
		



	def win(self):

		self.win_function()
		self.win_listbox()
		self.win_button_page()

	def win_button_page(self):
		
		def previous_page():
			current_page = int(self.page_folder.get())
			if current_page == 0 :
				return
			else:
				current_page -= 1
				self.page_folder.delete(0, END)
				self.page_folder.insert(END, current_page)
				self.check_url()


		def next_page():
			current_page = int(self.page_folder.get())
			
			current_page += 1
			self.page_folder.delete(0, END)
			self.page_folder.insert(END, current_page)
			self.check_url()

		frame = Frame(self.master)
		Button(frame, text = '< Previous Page', command = previous_page).pack(side =  LEFT)
		Button(frame, text = 'Next Page >', command = next_page).pack(side = LEFT)
		frame.pack(side = TOP)

	def win_function(self):
		function_frame = Frame(self.master)

		search_frame = Frame(function_frame)
		Button(search_frame, text = 'Search', command =lambda: threading.Thread(target = self.btn_search).start()).pack(side = RIGHT)
		self.q_search = Entry(search_frame, width = 50)
		self.q_search.pack(side = RIGHT)
		search_frame.pack(side = TOP, expand = True, fill = BOTH)



		input_link_frame = Frame(function_frame)
		Button(input_link_frame, text = '<', command = self.prev_buffer).pack(side = LEFT)
		Button(input_link_frame, text = 'Paste link: ', command = lambda: [ self.input_link.delete(0, END), self.input_link.insert(0,pyperclip.paste())]  ).pack(side = LEFT)
		self.input_link = Entry(input_link_frame, width = 100)
		self.input_link.pack(side = LEFT)
		self.button_link = Button(input_link_frame, text = 'Check !', command = self.check_url)
		self.button_link.pack(side = LEFT)
		Button(input_link_frame, text = '>', command = self.next_buffer).pack(side = LEFT)
		input_link_frame.pack(side = TOP, expand = True, anchor = CENTER)


		name_folder_frame = Frame(function_frame)
		Label(name_folder_frame,text = 'Folder: ', font = ('',14)).pack(side = LEFT)
		self.name_main_folder =  Entry(name_folder_frame, font = ('', 14), width = 50)
		self.name_main_folder.pack(side = LEFT)
		name_folder_frame.pack(side = TOP, fill = X)



		play_link_frame = Frame(function_frame)
		Button(play_link_frame, text = 'Get Link', command = self.get_link_item).pack(side = LEFT)
		Label(play_link_frame, text = 'URL Download: ').pack(side = LEFT)
		self.url_download = Entry(play_link_frame, width = 70,justify = LEFT )
		self.url_download.pack(side = LEFT)
		self.button_play = Button(play_link_frame, text ='Play', command = lambda: threading.Thread(target=self.play_media, args=(self.url_download.get(),)).start() )
		self.button_play.pack(side = LEFT)
		self.button_cp_link = Button(play_link_frame, text = 'Copy link', command = lambda:pyperclip.copy(self.url_download.get()))
		self.button_cp_link.pack(side = LEFT)
		play_link_frame.pack(side = TOP,fill = BOTH )

		status_frame = Frame(function_frame)
		Label(status_frame, text = 'Count: ').pack(side = LEFT)
		self.count_folder = Entry(status_frame, width = 5,  justify =RIGHT)
		self.count_folder.pack(side = LEFT)
		Label(status_frame, text = 'Page: ').pack(side = LEFT)
		self.page_folder = Entry(status_frame, width = 5, justify = RIGHT)
		self.page_folder.pack(side = LEFT)
		self.page_folder.insert(END, '0')
		Label(status_frame, text = 'Max Items/Page').pack(side = LEFT)
		self.items_per_pages = Entry(status_frame, width = 5, justify =RIGHT )
		self.items_per_pages.pack(side = LEFT)
		self.items_per_pages.insert(END, '60')
		Label(status_frame, text = 'URL item:').pack(side = LEFT)
		self.url_item = Entry(status_frame, width = 50, justify = LEFT)
		self.url_item.pack(side = LEFT)
		Button(status_frame, text = 'Copy URL', command = lambda: pyperclip.copy(self.url_item.get())).pack(side = LEFT)
		status_frame.pack(side = TOP, fill = BOTH)

		favorites_frame = Frame(function_frame)
		Button(favorites_frame, text = 'Add to Favorites', command = lambda:threading.Thread(target = self.add_favorites).start() ).pack(side = LEFT)
		Button(favorites_frame, text = 'Delete Favorites Item', command = self.delete_favorites).pack(side = LEFT)
		Button(favorites_frame, text = 'Show List Favorites', command = lambda:[self.get_favorites(),self.save_buffer()] ).pack(side = LEFT)
		

		favorites_frame.pack(side = TOP, fill  = X)

		function_frame.pack(side=TOP, fill = X)

	def win_listbox(self):
		listbox_main = Frame(self.master)
		listbox_main.pack(side = TOP, fill = BOTH, expand = True)

		self.listbox_frame = Frame(listbox_main )
		listbox_paned = PanedWindow(self.listbox_frame)

		self.scrollbar = Scrollbar(self.listbox_frame)
		self.scrollbar.pack(side = RIGHT,fill = Y)

		name_frame = Frame(listbox_paned)
		Label(name_frame,text = 'Name').pack(side = TOP)
		self.listbox_name = Listbox(name_frame, width = 150, activestyle = 'none', selectforeground='Black')
		self.listbox_name.pack(side = TOP, fill = BOTH, expand = True)		
		self.listbox_name.config(yscrollcommand = self.scrollbar.set)
		self.listbox_name.bind('<<ListboxSelect>>' , self.handles_click_item)
		self.listbox_name.bind("<Double-Button-1>", self.handle_dbclick_item)
		self.listbox_name.bind("<MouseWheel>", lambda evetn: "break")
		listbox_paned.add(name_frame)

		size_frame = Frame(listbox_paned)
		Label(size_frame,text = 'Size').pack(side = TOP)
		self.listbox_size = Listbox(size_frame,width = 20,activestyle = 'none', selectforeground='Black')
		self.listbox_size.pack(side = TOP, fill = BOTH, expand = True)		
		self.listbox_size.config(yscrollcommand = self.scrollbar.set)
		self.listbox_size.bind("<MouseWheel>", lambda evetn: "break")
		listbox_paned.add(size_frame)

		file_type_frame = Frame(listbox_paned)
		Label(file_type_frame,text = 'Type').pack(side = TOP)
		self.listbox_file_type = Listbox(file_type_frame,width = 20,activestyle = 'none', selectforeground='Black')
		self.listbox_file_type.pack(side = TOP, fill = BOTH, expand = True,)		
		self.listbox_file_type.config(yscrollcommand = self.scrollbar.set)
		self.listbox_file_type.bind("<MouseWheel>", lambda evetn: "break")
		listbox_paned.add(file_type_frame)
		
		self.scrollbar.config(command = self.OnVsb)	

		listbox_paned.pack(side = TOP, fill = BOTH, expand = True)
		self.listbox_frame.pack(side =  TOP, fill = BOTH, expand = True)

		self.giff_frame = GifFrame(listbox_main, 'images/loading.gif')
		self.giff_frame.pack_forget()


	def add_favorites(self):
		url_favorites = self.url_item.get()
		data_favorites= self.load_favorites()
		data_session = self.load_data()
		current_favorites = self.get_file_infor(url_favorites,data_session['token'], data_session['session'] )
		current_favorites['furl'] = url_favorites
		data_favorites.append(current_favorites)
		self.save_favorites(data_favorites)

	def delete_favorites(self):
		curselection = self.listbox_name.curselection()
		if int(curselection[0])%2 == 0:
			del self.items[int(curselection[0]/2)]
			self.save_favorites(self.items)
			self.del_all_win()
			self.insert_listbox()

	def get_favorites(self):
		self.items = self.load_favorites()
		self.del_all_win()
		for item in self.items:
			self.insert_item_listbox(item)



	def threading_search(self):
		self.del_all_win()
		items_search = self.get_items_search(self.q_search.get())
		data = self.load_data()
		self.items = []
		for item in items_search:
			try:
				temp = self.get_file_infor(item,data['token'], data['session'])
				temp['furl'] = item
				self.items.append(temp)
			except: pass

		self.insert_listbox()



	def btn_search(self):
		self.listbox_frame.pack_forget()
		self.giff_frame.pack(fill = BOTH, expand = True)
		t = threading.Thread(target = self.threading_search)
		t.start()
		t.join()
		self.listbox_frame.pack(fill = BOTH, expand = True)
		self.giff_frame.pack_forget()
		self.save_buffer()


		



	def del_all_win(self):
		self.input_link.delete(0, END)
		self.name_main_folder.delete(0,END)
		self.url_download.delete(0, END)
		self.count_folder.delete(0, END)
		self.url_item.delete(0,END)
		self.listbox_name.delete(0,END)
		self.listbox_size.delete(0,END)
		self.listbox_file_type.delete(0,END)

	def OnVsb(self, *args):
		self.listbox_name.yview(*args)
		self.listbox_size.yview(*args)
		self.listbox_file_type.yview(*args)


