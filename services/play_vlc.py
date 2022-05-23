import os
class PLayVLC:
	def play_media(self, **kwargs):
		print(kwargs['path_sub'])


		if  kwargs['path_sub'] != '':
			run = os.system(f"cd C:\\Program Files\\VideoLAN\\VLC\\ && vlc {kwargs['url']} --sub-file={kwargs['path_sub']}")
			
			if run ==  1:
				run = os.system(f"cd C:\\Program Files (x86)\\VideoLAN\\VLC\\ && vlc {kwargs['url']} --sub-file={kwargs['path_sub']}")

			if run == 1:
				return False

		else:

			run = os.system(f"cd C:\\Program Files\\VideoLAN\\VLC\\ && vlc {kwargs['url']}")
				
			if run ==  1:
				run = os.system(f"cd C:\\Program Files (x86)\\VideoLAN\\VLC\\ && vlc {kwargs['url']}")

			if run == 1:
				return False

