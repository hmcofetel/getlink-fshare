from tkinter import *


class GifFrame(Frame):
	def __init__(self, master, path, **kwargs):
		Frame.__init__(self,master, **kwargs)
		self.path = path
		self.framelist = []      
		self.frame_index = 0 
		self.count = 0
		self.anim = None
		self.list_gif_frames =[]
		self.load_frame()
		self.lb = Label(self, image = "", **kwargs)
		self.lb.pack()
		
		
	def pack(self,*args,**kwargs):
		super().pack();
		self.animate_gif(0);

	def pack_forget(self):
		super().pack_forget();
		self.stop_gif();

		
	def animate_gif(self, count):  
	    self.lb.config(image = self.framelist[self.count])
	    self.count +=1	        
	    if self.count > self.last_frame:
	        self.count = 0 
	    self.anim = self.after(20, lambda :self.animate_gif(self.count))    

	def load_frame(self):
		while True:
		    try:
		        part = 'gif -index {}'.format(self.frame_index)
		        self.frame = PhotoImage(file=self.path, format=part)
		    except:
		        self.last_frame = self.frame_index - 1   
		        break               
		    self.framelist.append(self.frame)
		    self.frame_index += 1 

	def stop_gif(self):
		try:
			self.after_cancel(self.anim)
		except:pass

