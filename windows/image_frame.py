from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import requests


class ImageFrame(Frame):
	def __init__(self, master, url, command, **kwargs):
		Frame.__init__(self,master,**kwargs)
		self.master = master
		self.pilImage = Image.open(BytesIO(requests.get(url).content))
		self.pilImage = self.pilImage.resize((178, 250))
		self.zoom = 1
		self.pixels_x, self.pixels_y = tuple([int(self.zoom * x)  for x in self.pilImage.size])
		self.image = ImageTk.PhotoImage(self.pilImage.resize((self.pixels_x, self.pixels_y)))
		Button(self,activebackground="black",bd = 0 ,image=self.image, command = command,**kwargs).pack()



if __name__ == '__main__':
	root = Tk()
	image =  ImageFrame(root,"https://thuvienhd.com/wp-content/uploads/2022/05/MV5BYWMyOWE0NmEtODg4My00NjY1LTk0NzAtNWEwYWY2YmE2NWRkXkEyXkFqcGdeQXVyNDM1ODc2NzE@._V1_SX1024_AL_-225x315.jpg")
	image.pack()
	root.mainloop()
