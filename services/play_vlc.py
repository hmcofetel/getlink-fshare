import os
class PLayVLC:
	def play_media(self, url):
		run = os.system(f"cd C:\\Program Files\\VideoLAN\\VLC\\ && vlc {url}")
			
		if run ==  1:
			run = os.system(f"cd C:\\Program Files (x86)\\VideoLAN\\VLC\\ && vlc {url}")

		if run == 1:
			return False

