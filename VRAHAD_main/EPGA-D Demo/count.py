from queue import Queue
from config import session
from models import Gi
import pickle

class gList(list):
	def empty(self):
		if len(self) == 0:
			return True
		else:
			return False

def getLast(Gi_query):
	# Deserialize Gi object from DB
	gi_obj = session.query(Gi).filter_by(gi = Gi_query).first()
	if gi_obj is None:
		return {'Gi':Gi_query,'cQueue':gList()}
	else:
		return gi_obj

def saveCount(countObject):
	# Save the serialzied object in DB
	session.add(countObject)
	session.commit()
