import sys
sys.path.append('../')
sys.path.append('../services')
import json
import time
from tkinter import *
from user import   APP_KEY,USER_AGENT
import tkinter.messagebox as tkmsg
from services.client import Client

class LoginWindow(Client):
	def __init__(self, master):
		super().__init__()
		self.master = master
		self.master.iconbitmap('logo.ico')
		self.menu()
		self.insert_data_entry()
		
	def menu(self):
		input_frame = Frame(self.master)

		text = Frame(input_frame)
		Label(text, text = 'Email: ').pack(side = TOP, anchor = W)
		Label(text, text = 'Password: ').pack(side =  TOP, anchor = W)
		text.pack(side = LEFT)

		entry_frame = Entry(input_frame)
		self.email_entry = Entry(entry_frame)
		self.email_entry.pack(side = TOP)
		self.password_entry = Entry(entry_frame)
		self.password_entry.pack(side = TOP)
		entry_frame.pack(side = LEFT)
		input_frame.pack(side = TOP) 

		button_frame = Frame(self.master)
		Button(button_frame, text = 'Login', command = self.login_w).pack(side = LEFT,fill = X)
		Button(button_frame, text = 'Close', command = self.master.destroy).pack(side = LEFT,fill = X)
		button_frame.pack(side = TOP)

	def login_w(self):
		login = self.login(self.email_entry.get(), self.password_entry.get())
		if login['msg'] == 'Login successfully!':
			data = {}
			data['email'] =  self.email_entry.get();
			data['password'] =  self.password_entry.get();
			data['timelog'] = str(time.time())
			data['session'] = login['session_id']
			data['token'] = login['token']
			self.save_data(data)
			tkmsg.showinfo(message = login['msg'], title = 'Success')
			self.master.destroy()

		else:
			tkmsg.showerror(message = login['msg'], title = 'Error !')

	def insert_data_entry(self):
		data = self.load_data()
		self.email_entry.insert(0,data['email'])
		self.password_entry.insert(0,data['password'])

	

