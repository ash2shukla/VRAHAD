from sys import version_info
from sys import path as sys_path
from json import dumps,loads,load
from time import time
from getInformation import getTID,getUDC,getIDC,getFDC,getPIP,getLOV,getOTP,getPIN,getLicenseKey,getTxnID,getCertificate,getSkey
from prepareRequest import prepareRequest
from parseResponse import parseResponse
from os import path
from datetime import datetime

master_dir = path.abspath(path.join(__file__,'..','..'))
sys_path.append(master_dir)

from SystemVerification.dmidecoder import linux_fingerprint

py_ver = version_info[0]

if py_ver == 3:
	from urllib.request import Request, urlopen
	from urllib.parse import urlencode
elif py_ver == 2:
	from urllib2 import Request, urlopen
	from urllib import urlencode

config = load(open('config.json'))

AadhaarURL = config['NirAadhaarURL']
KeyServerURL = config['KeyServerURL']

def currentISO8601():
	'''
	Returns current time stamp in ISO8601 format YYYY:MM:DDTHH:MM:SS
	'''
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
	'''
	Both python version compatible bytes() function.
	'''
	if py_ver == 3:
		return bytes(string,'utf-8')
	elif py_ver == 2:
		return bytes(string)

def AuthInit(uid="111111111111",lang="06",name="",lname="",gender="",dob="",dobt="",age="",phone="",email="",\
			co="",house="",street="",lm="",lco="",vtc="",subdist="",dist="",state="",pc="",po="",\
			tkntype="",tknvalue="",\
			av="",lav="",otp="",\
			bio_dict={},\
			is_otp=False,\
			is_pin=False,\
			is_asa_cert=False):
	'''
	Initialize Authentication.
	Gets user input and calls prepareRequest.
	'''
	device =  linux_fingerprint()
	ver = "1.6"
	ac = "TEST_CENTER" 	# auaID
	sa = "VRAHAD" # sa = ac as we don't have subdivisons'
	aua = "TEST_CENTER"
	is_Fingerprint = True
	is_Iris = True
	lot = "G" 		# can also set it to P
	ki = ""			# OtherDocuments/DigitalCertificates_ for other info
	dtype="X" 		# can be P for protobuff

	if name != "":
		ims = "E" # ms for Pi (Identity)
		imv = "" # Pecentage match if partial ms for Pi
	else:
		ims = ""
		imv = ""

	if lname != "":
		ilmv = "90" # Percentage match if name lname of person given in Pi
	else:
		ilmv = ""

	if bio_dict is not "":
		bt = ','.join(bio_dict.keys())

	if av is not "":
		fams = "P" # ms for Pfa (Full Address)
		famv = "60" # mv for Pfa
	else:
		fams = ""
		famv = ""

	if lav != "":
		falmv="60" # mv for Pfa in language
	else:
		falmv = ""

	if bio_dict !={}:
		bt = ','.join(bio_dict.keys())

	Auth = {}
	Auth['uid'] = uid
	Auth['tid'] = getTID()
	Auth['ac'] = ac
	Auth['sa'] = sa
	Auth['ver'] = ver
	Auth['txn'] = getTxnID(aua,uid)
	Auth['lk'] = getLicenseKey(aua)

	Tkn = {}
	Tkn['type']=tkntype
	Tkn['value']=tknvalue

	Meta = {}
	Meta['udc'] = getUDC()
	Meta['fdc'] = getFDC(is_Fingerprint)
	Meta['idc'] = getIDC(is_Iris)
	Meta['pip'] = getPIP()
	Meta['lot'] = lot
	Meta['lov'] = getLOV(lot)

	Skey = {}
	if not is_asa_cert:
		Skey['ci'] = getCertificate('expiry')
	else:
		Skey['ci'] = ""
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
	Pa['lco'] = lco
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
	Pv['otp'] = otp
	Pv['pin'] = getPIN(is_pin)

	Uses = {}
	isNone = lambda lst : 'N' if all(i=="" for i in lst) else 'Y'
	Uses['pi'] = isNone(Pi.values())
	Uses['pa'] = isNone(Pa.values())
	Uses['pfa'] = isNone(Pfa.values())
	Uses['bio'] = 'N' if bio_dict == {} else 'Y'
	Uses['bt'] = bt
	Uses['pin'] = 'Y' if is_pin else 'N'
	Uses['otp'] = 'Y' if is_otp else 'N'
	skey,EncSkey = getSkey()
	request = prepareRequest(Auth = Auth,Uses = Uses,Tkn=Tkn,Meta = Meta,Skey = Skey,Data = Data,\
							 Demo = Demo,Pid = Pid,Pi = Pi,Pa = Pa,Pfa = Pfa,Bios = bio_dict,\
							 Pv = Pv,aua=aua,is_asa_cert=is_asa_cert,skey=skey,EncSkey=EncSkey)

	# Prepare the request and send it to ASA
	# ASA will return the response which we would parse
	r = Request(KeyServerURL+"forwardAuthReq/",data=request)

	# Send the device header along with the request
	r.add_header('X-DEVICE',device)
	r.add_header('X-AC',ac)
	response = urlopen(r).read()

	parseResponse(response)

def OTPInit(is_otp,ch):
	device =  linux_fingerprint()
	ver = "1.6"
	ac = "TEST_CENTER"
	sa = "VRAHAD"
	getOTP(is_otp,ver,ac,uid,device,sa,ch)

if __name__ == "__main__":
	uid = "903298497974"
	# Name of the person to Authenticate in English
	name = "Ashish Shukla"
	# Name of the person to authenticate in Native Language
	lname = u"आशीष शुक्ला"
	gender = "M"
	dob = "1996"
	# Date of birth is verified/declared/approximate V/D/A
	dobt = "V"
	age = "22"
	phone="919818611161"
	email="ash2shukla@gmail.com"
	lang = "06"
	co="Vidyadhar Shukla"
	house= "520"
	street= "Raibareily Road"
	lco= u"विद्याधर शुक्ला"
	vtc= "C"
	dist= "Unnao"
	subdist="Unnao City"
	state= "Uttar Pradesh"
	pc= "209801"
	po= "Unnao H.O."
	av = "520 Indira Nagar Raibareily Road Unnao"
	lav = u"520 इन्दिरा नगर रायबरेली रोड उन्नाव"
	# Pass bio as a dict of type: [ (posh(key),encoded biometric (value))]
	bio_dict = {"FMR":[("LEFT_THUMB","ABCD5"),("RIGHT_THUMB","EFGH5")],
	"IIR":[("LEFT_IRIS","ABCDEFGH")]}
	# bio_dict format = {"type":[("posh","value") ... ("posh","value")]}
	is_otp= True
	is_pin = False


	# if it is true then ASA will sign the AuthRequest
	is_asa_cert = False
	#OTPInit(is_otp,'11')

	# Invoke OTPInit first then ask the customer to enter the OTP somewhere,
	# With the value of OTP Invoke the AuthInit function

	AuthInit(uid=uid,otp="952075",lang=lang,subdist=subdist,name=name,lname=lname,gender=gender,dob=dob,age=age,phone=phone,email=email,\
		co=co,house=house,street=street,lco=lco,vtc=vtc,dist=dist,state=state,pc=pc,po=po,av=av,lav=lav,\
		bio_dict=bio_dict,is_otp=is_otp,is_pin=is_pin,is_asa_cert=is_asa_cert)
