from windows.login_window import LoginWindow
from windows.main_window import MainWindow
from services.data import Data
from tkinter import *
import time



class App(Data):
	def __init__(self):
		self.check_session()
		self.run_app()


	def run_login(self):
		root = Tk()
		login = LoginWindow(root)
		root.mainloop()


	def check_session(self):
		data = self.load_data()
		if data['timelog'] == '' or time.time() - float(data['timelog'])  >= 21600:
			return False
		else: return True
			
	def run_app(self):
		if self.check_session():
			root  = Tk()
			app = MainWindow(root)
			root.mainloop()

		else:
			self.run_login()				
			if self.check_session():
				root  = Tk()
				app = MainWindow(root)
				root.mainloop()



