from sys import version_info
import xml
from json import dumps,loads
from time import time
from hashlib import sha256

py_ver = version_info[0]

if py_ver == 3:
	from urllib.request import Request, urlopen
	from urllib.parse import urlencode
elif py_ver == 2:
	from urllib2 import Request, urlopen
	from urllib import urlencode

def to_bytes(string):
	if py_ver == 3:
		return bytes(string,'utf-8')
	elif py_ver == 2:
		return bytes(string)

def getAuthURL(*args):
	URL = "http://"+('/'.join(args))
	return URL

def getAuth(XML_request,base_URL,api_ver,auaID,uid_0,uid_1,asalk):
	r = Request(getAuthURL(base_URL,api_ver,auaID,uid_0,uid_1,asalk))
	return urlopen(r,to_bytes(urlencode({'data':XML_request}))).read().decode('utf-8')

def prepareRequest(Auth = ["public","111111111111","None"],\
					Uses = ["YYNNNN",""],
					Tkn=["",""],
					):
	return ''

def parseResponse(arg):
	print(loads(arg))

def getTxnID(uid):
	# prepare a transaction ID based on UID and timestamp
	str(int(time()))+uid

def getLicenseKey(sa):
	# Client will recieve LicenseKeys from AUA
	# AUA recieves it from Aadhaar server
	# Here AUA = our KeyServer of VRAHAD
	# See AUA module in PostgresREST
	LKey = urlopen(Request('http://localhost:8000/getKey/'+sa)).read().decode('utf-8')
	print(loads(LKey))


if __name__ == "__main__":
	base_URL = "localhost:8001"
	asalk = "ASALK_TEST_KEY"
	ver = "1.2"
	ac = "VRAHAD" # auaID
	sa = "TEST_CENTER"
	uid = "903298497974"
	bt= "FMR,FIR,IIR"
	uses_yn = "YYYYNY"
	txn = getTxnID(uid)
	lk = getLicenseKey(sa) # getLicenseKey from AUA

	request = prepareRequest(Auth=[ac,uid,asalk],\
							# pi,pa,pfa,bio,pin,otp, if bio true then bt
							# As pi,pa,pfa,bio,pin,otp is 1/0 we can transmit "YNYNYN" <- like string
							# Let all be True for this case except pin, as its not used by clients except UIDAI itself
							# Let the value be FMR,FIR, and IIR all 3 for bt
							 Uses=[uses_yn,bt],\
							 # Tkn feature is ambiguous what it does etc. So leave it blank for now
							 Tkn = [],\

							  )
	response = getAuth(request,base_URL,ver,ac,uid[0],uid[1],asalk)
	parseResponse(response)
