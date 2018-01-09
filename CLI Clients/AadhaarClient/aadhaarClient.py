from sys import version_info
import xml
from json import dumps,loads
from time import time
from hashlib import sha256
from getInformation import getTID,getUDC,getIDC,getFDC,getPIP,getLOV,getSkey,\
						getOTP,getPIN,getLicenseKey,getCertificate
from datetime import datetime
import lxml.etree as etree

py_ver = version_info[0]

if py_ver == 3:
	from urllib.request import Request, urlopen
	from urllib.parse import urlencode
elif py_ver == 2:
	from urllib2 import Request, urlopen
	from urllib import urlencode

def currentISO8601():
	now_ist = datetime.now()
	year = str(now_ist.year)
	month = str(now_ist.month)
	day = str(now_ist.day)
	hour = str(now_ist.hour)
	minute = str(now_ist.minute)
	second = str(now_ist.second)

	if len(month) == 1:
		month = '0'+month

	if len(day) == 1:
		day = '0'+day

	date = '-'.join([year,month,day])
	_time = ':'.join([hour,minute,second])

	return date+"T"+_time

def to_bytes(string):
	if py_ver == 3:
		return bytes(string,'utf-8')
	elif py_ver == 2:
		return bytes(string)

def getAuthURL(*args):
	URL = "http://"+('/'.join(args))
	return URL

def getAuth(XML_request,baseURL,api_ver,auaID,uid_0,uid_1,asalk):
	r = Request(getAuthURL(baseURL,api_ver,auaID,uid_0,uid_1,asalk))
	return urlopen(r,to_bytes(urlencode({'data':XML_request}))).read().decode('utf-8')

def createNode(nodeName, elements, values,text = None):
	node = etree.Element(nodeName)
	for i,j in zip(elements,values):
		if j is not None:
			node.set(i,j)
	if text is not None:
		node.text = text
	return node

def prepareRequest(Auth = {},\
					Uses = {},\
					Tkn = {},\
					Meta = {},\
					Skey = {},\
					Data = {},\
					Demo = {},\
					# Pid has values as timestamp ISO8601 and version i.e. 1.0
					Pid = {},\
					Pi = {},\
					Pa = {},\
					Pfa = {},\
					Bios = {},\
					Pv = {},\
					asa=""):

	AuthNode = createNode('Auth',Auth.keys(),Auth.values())
	UsesNode = createNode('Uses',Uses.keys(),Uses.values())
	TknNode = createNode('Tkn',Tkn.keys(),Tkn.values())
	MetaNode = createNode('Meta', Meta.keys(),Meta.values())
	SkeyNode = createNode('Skey',Skey.keys(),Skey.values(),getSkey(asa))
	DataNode = createNode('Data',Data.keys(),Data.values())
	PidNode = createNode('Pid',Pid.keys(),Pid.values())
	DemoNode = createNode('Demo',Demo.keys(),Demo.values())
	PiNode = createNode('Pi',Pi.keys(),Pi.values())
	PaNode = createNode('Pa',Pa.keys(),Pa.values())
	PfaNode = createNode('Pfa',Pfa.keys(),Pfa.values())
	PvNode = createNode('Pv',Pv.keys(),Pv.values())
	BiosNode = createNode('Bios',[],[])
	HmacNode = createNode('Hmac',[],[])
	SignatureNode = createNode('Signature',[],[])

	for i,lst in zip(Bios.keys(),Bios.values()):
		for j,k in lst:
			BiosNode.append(createNode('Bio',["type","posh"],[i,j],k))


	AuthNode.append(UsesNode)
	AuthNode.append(TknNode)
	AuthNode.append(MetaNode)
	AuthNode.append(SkeyNode)

	DemoNode.append(PiNode)
	DemoNode.append(PaNode)
	DemoNode.append(PfaNode)

	PidNode.append(DemoNode)
	PidNode.append(BiosNode)

	print(etree.tostring(AuthNode,pretty_print=True).decode('utf-8'))
	return ''

def parseResponse(arg):
	print(loads(arg))

def getTxnID(uid):
	# prepare a transaction ID based on UID and timestamp
	return str(int(time()))+uid

def AuthInit(uid="111111111111",lang="06",name=None,lname=None,gender=None,dob=None,dobt=None,age=None,phone=None,email=None,\
			co=None,house=None,street=None,lm=None,loc=None,vtc=None,subdist=None,dist=None,state=None,pc=None,po=None,\
			av=None,lav=None,\
			bio_dict=None,\
			is_otp=False,\
			is_pin=False):

	baseURL = "localhost:8001"
	asalk = "ASALK_TEST_KEY"
	ver = "1.6"
	ac = "VRAHAD" 	# auaID
	sa = "VRAHAD" # sa = ac as we don't have subdivisons'
	asa = "TEST_CENTER"
	is_Fingerprint = True
	is_Iris = True
	lot = "G" 		# can also set it to P
	ci = "01082019" # See OtherDocuments/DigitalCertificates for Expiry and
	ki = None		# OtherDocuments/DigitalCertificates_ for other info
	dtype="X" 		# can be P for protobuff

	if name is not None:
		ims = "P" # ms for Pi (Identity)
		imv = "90" # Pecentage match if partial ms for Pi
	else:
		ims = None
		imv = None

	if lname is not None:
		ilmv = "90" # Percentage match if name lname of person given in Pi
	else:
		ilmv = None

	if bio_dict is not None:
		bt = ','.join(bio_dict.keys())

	if av is not None:
		fams = "P" # ms for Pfa (Full Address)
		famv = "60" # mv for Pfa
	else:
		fams = None
		famv = None

	if lav is not None:
		falmv="60" # mv for Pfa in language
	else:
		falmv = None

	if bio_dict is not None:
		bt = ','.join(bio_dict.keys())

	Auth = {}
	Auth['uid'] = uid
	Auth['tid'] = getTID()
	Auth['ac'] = ac
	Auth['sa'] = sa
	Auth['ver'] = ver
	Auth['txn'] = getTxnID(uid)
	Auth['lk'] = getLicenseKey(asa)

	Meta = {}
	Meta['udc'] = getUDC()
	Meta['fdc'] = getFDC(is_Fingerprint)
	Meta['idc'] = getIDC(is_Iris)
	Meta['pip'] = getPIP()
	Meta['lot'] = lot
	Meta['lov'] = getLOV(lot)

	Skey = {}
	Skey['ci'] = getCertificate('expiry')
	Skey['ki'] = ki

	Data = {}
	Data['type'] = dtype

	Pid = {}
	Pid['ts'] = currentISO8601()
	Pid['ver'] = "1.0"

	Demo = {}
	Demo['lang'] = lang

	Pi = {}
	Pi['ms'] = ims
	Pi['mv'] = imv
	Pi['name'] = name
	Pi['lname'] = lname
	Pi['lmv'] = ilmv
	Pi['gender'] = gender
	Pi['dob'] = dob
	Pi['dobt'] = dobt
	Pi['age'] = age
	Pi['phone'] = phone
	Pi['email'] = email

	Pa = {}
	Pa['ms'] = "E"
	Pa['co'] = co
	Pa['house'] = house
	Pa['street'] = street
	Pa['lm'] = lm
	Pa['loc'] = loc
	Pa['vtc'] = vtc
	Pa['subdist'] = subdist
	Pa['dist'] = dist
	Pa['state'] = state
	Pa['pc'] = pc
	Pa['po'] = po

	Pfa = {}
	Pfa['ms'] = fams
	Pfa['mv'] = famv
	Pfa['av'] = av
	Pfa['lav'] = lav
	Pfa['lmv'] = falmv

	Pv = {}
	Pv['otp'] = getOTP(is_otp,baseURL,ver,ac,uid[0],uid[1],asalk)
	Pv['pin'] = getPIN(is_pin)

	Uses = {}
	isNone = lambda lst : 'N' if all(i==None for i in lst) else 'Y'
	Uses['pi'] = isNone(Pi.values())
	Uses['pa'] = isNone(Pa.values())
	Uses['pfa'] = isNone(Pfa.values())
	Uses['bio'] = 'N' if bio_dict == None else 'Y'
	Uses['bt'] = bt
	Uses['pin'] = 'Y' if is_pin else 'N'
	Uses['otp'] = 'Y' if is_otp else 'N'

	request = prepareRequest(Auth = Auth,\
							 Uses = Uses,\
							 Meta = Meta,\
							 Skey = Skey,\
							 Data = Data,\
							 Demo = Demo,\
							 # Pid has values as timestamp ISO8601 and version i.e. 1.0
							 Pid = Pid,\
							 Pi = Pi,\
							 Pa = Pa,\
							 Pfa = Pfa,\
							 Bios = bio_dict,\
							 Pv = Pv,\
							 asa=asa)

	response = getAuth(request,baseURL,ver,ac,uid[0],uid[1],asalk)
	parseResponse(response)

if __name__ == "__main__":
	uid = "903298497974"
	# Name of the person to Authenticate in English
	name = "Ashish Shukla"
	# Name of the person to authenticate in Native Language
	lname = u"आशीष शुक्ला"
	gender = "M"
	dob = "19960808"
	# Date of birth is verified/declared/approximate V/D/A
	dobt = "V"
	age = "21"
	phone="919818611161"
	email="ash2shukla@gmail.com"
	lang = "06"
	co="VidyaDhar Shukla"
	house= "520"
	street= "Raibareily Road"
	loc= "Indira Nagar"
	vtc= "Unnao City"
	dist= "Unnao"
	state= "Uttar Pradesh"
	pc= "209801"
	po= "Unnao H.O."
	av = "520 Indira Nagar Raibareily Road Unnao"
	lav = u"520 इन्दिरा नगर रायबरेली रोड उन्नाव"
	# Pass bio as a dict of type: [ (posh(key),encoded biometric (value))]
	bio_dict = {"FMR":[("LEFT_THUMB","ABCD5"),("RIGHT_THUMB","EFGH5")],
	"FIR":[("LEFT_THUMB","ABCD5")]}
	# bio_dict format = {"type":[("posh","value") ... ("posh","value")]}
	is_otp= True
	is_pin = False

	AuthInit(uid=uid,lang=lang,name=name,lname=lname,gender=gender,dob=dob,dobt=dobt,age=age,phone=phone,email=email,\
		co=co,house=house,street=street,loc=loc,vtc=vtc,dist=dist,state=state,pc=pc,po=po,av=av,lav=lav,\
		bio_dict=bio_dict,is_otp=is_otp,is_pin=is_pin)
