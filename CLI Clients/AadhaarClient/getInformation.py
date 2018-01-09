# Device returns Terminal ID , device would have it already embedded
# it would return the same on calling getTID function
from sys import version_info
from os import urandom
from base64 import b64encode,b64decode
from json import dumps,loads
from OpenSSL.crypto import load_certificate,FILETYPE_PEM

py_ver = version_info[0]

if py_ver == 3:
	from urllib.request import Request, urlopen
	from urllib.parse import urlencode
elif py_ver == 2:
	from urllib2 import Request, urlopen
	from urllib import urlencode

def getCertificate(field,cert_path='aua.crt'):
	cert_raw = open(cert_path,'rt').read()
	cert = load_certificate(FILETYPE_PEM, cert_raw)
	if field == "expiry":
		return cert.get_notAfter()
	elif field == "raw":
		return '\n'.join(open(cert_path,'rt').read().split('\n')[1:-2])

def getTID(**kwargs):
	# Implement any logic for verifying the request
	return "TEST_TID"

def getUDC(**kwargs):
	# [vid]= XXXX (4 digits num)
	# date of deployment = "111111" (6 digits num)
	# serial = XXXXXXXXXX ( 10 digits alnum)
	return "XXXX111111XXXXXXXXXX"

def getFDC(is_Fingerprint,**kwargs):
	# Implement logic for retrieving Fingerprint Device Code
	if is_Fingerprint:
		return "FFFFFFFFFF"
	else:
		return "NA"

def getIDC(is_Iris,**kwargs):
	# Implement logic for retrieving Iris Device code
	if is_Iris:
		return "IIIIIIIIII"
	else:
		return "NA"

def getPIP(**kwargs):
	try:
		url = "http://ip.42.pl/raw"
		return urlopen(Request(url)).read().decode('utf-8')
	except:
		return "NA"

def getLatLngAlt():
	# Implement logic for getting current latitude longitude and altitude(if possible)
	lat = "26.5393" # 15 chars
	lon = "80.4878" # 15 chars max
	alt = "98" # 7 chars in meters
	return ','.join([lat,lon,alt])

def getLOV(lot,**kwargs):
	if lot == "G":
		return getLatLngAlt()
	elif lot == "P":
		# return the pincode
		return "209801"

def getSkey(asa):
	url = 'http://localhost:8000/getSession/'+asa
	AES256 = urandom(32)
	AES256ToStr = b64encode(AES256).decode('utf-8')
	# Request AUA server to create Session ID
	r = Request(url,data=bytes(dumps({'SessionID':AES256ToStr}),'utf-8'))
	r.add_header('Content-Type','application/json')
	Skey = loads(urlopen(r).read().decode('utf-8'))
	return Skey

def getOTP(is_otp,base_URL,ver,ac,uid_0,uid_1,asalk):
	if is_otp:
		URL = "http://"+('/'.join([base_URL,'otp',ver,ac,uid_0,uid_1,asalk]))
		print(URL)
	else:
		return None

def getPIN(is_pin):
	if is_pin:
		return "XXXXXX"
	else:
		return None

def getLicenseKey(asa):
	# Client will recieve LicenseKeys from AUA
	# AUA recieves it from Aadhaar server
	# Here AUA = our KeyServer of VRAHAD
	# See AUA module in PostgresREST
	LKey = urlopen(Request('http://localhost:8000/getKey/'+asa)).read().decode('utf-8')
	LKey = loads(LKey)
	return LKey
