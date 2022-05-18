import sys
sys.path.append('../')
from user import USER_AGENT, APP_KEY,GG_KEY, CX
from services.fshare import Fshare
from services.google_search import GoogleSearch
from services.data import Data
class Client(Fshare, GoogleSearch , Data):
	def __init__(self):
		Fshare.__init__(self,APP_KEY,USER_AGENT)
		GoogleSearch.__init__(self,GG_KEY, CX)