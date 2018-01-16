from sys import version_info
from sys import path as sys_path
from json import dumps,loads,load
from time import time
from prepareRequest import prepareRequest
from getInformation import *
from parseResponse import parseResponse
from os import path
from lxml import etree
from hashlib import sha256
from Utils import *


master_dir = path.abspath(path.join(__file__,'..','..'))
sys_path.append(master_dir)

from SystemVerification.dmidecoder import linux_fingerprint
from urllib.request import Request, urlopen
from urllib.parse import urlencode

ver = "1.6"
ac = "TEST_CENTER" 	# auaID
sa = "VRAHAD" # sa = ac as we don't have subdivisons'
aua = "TEST_CENTER"
is_Fingerprint = True
is_Iris = True
lot = "G" 		# can also set it to P
ki = ""			# OtherDocuments/DigitalCertificates_ for other info
dtype="X"
is_otp =True
is_pin = False
is_asa_cert= False
tkntype= ""
tknvalue = ""
lot = "G"

# create the Skey and save it for session
skey,EncryptedSkey = getSkey()

isNone = lambda lst : 'N' if all(i=="" for i in lst) else 'Y'

def createTknNode():
	elements = ['type','value']
	values = [tkntype,tknvalue]

	node = createNode('Tkn',elements,values)

	return node

def createMetaNode():
	elements = ['udc','fdc','idc','pip','lot','lov']
	values = [getUDC(),getFDC(is_Fingerprint),getIDC(is_Iris),getPIP(),lot,getLOV(lot)]

	node = createNode('Meta',elements, values)

	return node

def createPiNode(JSONInput):
	if JSONInput['name'] != "":
		ims = "E" # ms for Pi (Identity)
		imv = "" # Pecentage match if partial ms for Pi
	else:
		ims = ""
		imv = ""

	if JSONInput['lname'] != "":
		ilmv = "90" # Percentage match if name lname of person given in Pi
	else:
		ilmv = ""

	elements = ['ms','mv','lmv']
	values = [ims,imv,ilmv]

	elements_from_json = ['name','lname','gender','dob','dobt','age','phone','email']

	[ (elements.append(i),values.append(JSONInput[i])) for i in elements_from_json ]

	node = createNode('Pi',elements,values)

	return node

def createPaNode(JSONInput):
	elements = ['ms']
	values = ["E"]

	elements_from_json = ['co','house','street','lm','lco','vtc','subdist','dist','state','pc','po']

	[ (elements.append(i),values.append(JSONInput[i])) for i in elements_from_json ]

	node = createNode('Pa',elements,values)

	return node

def createPfaNode(JSONInput):
	if JSONInput['av'] is not "":
		fams = "P" # ms for Pfa (Full Address)
		famv = "60" # mv for Pfa
	else:
		fams = ""
		famv = ""

	if JSONInput['lav'] != "":
		falmv="60" # mv for Pfa in language
	else:
		falmv = ""

	elements = ['ms','mv','lmv']
	values = [fams,famv,falmv]

	elements_from_json = ['av','lav']

	[ (elements.append(i),values.append(JSONInput[i])) for i in elements_from_json ]

	node = createNode('Pfa',elements,values)

	return node

def createPvNode(otp):
	elements = ['otp','pin']
	values = [otp,getPIN(is_pin)]

	node = createNode('Pv',elements,values)

	return node

def createDemoNode(Pi,Pa,Pfa,lang):
	DemoNode = createNode('Demo',['lang'],[lang])
	DemoNode.append(Pi)
	DemoNode.append(Pa)
	DemoNode.append(Pfa)

	return DemoNode

def createPIDNode(DemoNode, BiosNode, PvNode):
	elements = ['ts','ver']
	values = [currentISO8601(), '1.0']

	PIDNode = createNode('Pid',elements,values)
	PIDNode.append(DemoNode)
	PIDNode.append(BiosNode)
	PIDNode.append(PvNode)

	return PIDNode

def createDataNode(PIDNode):
	elements = ['type']
	values = [dtype]
	text = encryptWithSession(skey, etree.tostring(PIDNode))

	return createNode('Data',elements, values,text)

def createHmacNode(PIDNode):
	digest = sha256(etree.tostring(PIDNode)).digest()
	text = encryptWithSession(skey,digest)

	return createNode('Hmac',[],[],text)

def createUsesNode(Pi,Pa,Pfa,bio_dict):
	usesBio = 'N' if bio_dict == {} else 'Y'
	bt = ','.join(bio_dict.keys())
	usesPin = 'Y' if is_pin else 'N'
	usesOtp = 'Y' if is_otp else 'N'

	elements = ['pi','pa','pfa','bio','bt','pin','otp']
	values = [isNone(Pi.values()), isNone(Pa.values()), isNone(Pfa.values()), usesBio, bt, usesPin, usesOtp]

	node = createNode('Uses', elements, values)

	return node

def createSignatureNode():
	if not is_asa_cert:
		return createNode('Signature',[],[],getCertificate('raw'))
	else:
		return createNode('Signature',[],[])

def createBiosNode(bio_dict):
	BiosNode = createNode('Bios',[],[])

	for i,lst in zip(bio_dict.keys(),bio_dict.values()):
		for j,k in zip(lst.keys(),lst.values()):
			BiosNode.append(createNode('Bio',["type","posh"],[i,j],k))

	return BiosNode

def createSkeyNode():
		return createNode('Skey',['ci'],[getCertificate('expiry')], EncryptedSkey)

def createAuthNode(JSONInput,NodeList):
	uid = JSONInput['uid']

	elements = ['uid','tid','ac','sa','ver','txn','lk']
	values = [uid,getTID(),aua,sa,ver,getTxnID(aua,uid),getLicenseKey(aua)]

	AuthNode = createNode('AuthNode',elements,values)

	[AuthNode.append(i) for i in NodeList]

	return AuthNode

def populateAuthXML(JSONInput,otp=""):
	# JSONInput must be in the same form as mentioned in Input.json
	# If some fields do not exist then simply put "" instead of value

	# if is_otp == true then value of otp must be input by user

	TknNode = createTknNode()
	MetaNode = createMetaNode()
	PiNode = createPiNode(JSONInput)
	PaNode = createPaNode(JSONInput)
	PfaNode = createPfaNode(JSONInput)
	PvNode = createPvNode(otp)
	DemoNode = createDemoNode(PiNode,PaNode,PfaNode,JSONInput['lang'])
	BiosNode = createBiosNode(JSONInput['bio_dict'])
	PIDNode = createPIDNode(DemoNode, BiosNode, PvNode)
	DataNode = createDataNode(PIDNode)
	UsesNode = createUsesNode(PiNode,PaNode,PfaNode,JSONInput['bio_dict'])
	SignatureNode = createSignatureNode()

	HmacNode = createHmacNode(PIDNode)
	SkeyNode = createSkeyNode()

	AuthNode = createAuthNode(JSONInput,[UsesNode,TknNode,MetaNode,SkeyNode,DataNode,HmacNode,SignatureNode])
	return etree.tostring(AuthNode)

def AuthRes(AuthXML):
	# Prepare the request and send it to ASA
	# ASA will return the response which we would parse
	device =  linux_fingerprint()
	r = Request(KeyServerURL+"forwardAuthReq/",data=AuthXML)

	# Send the device header along with the request
	r.add_header('X-DEVICE',device)
	r.add_header('X-AC',ac)
	response = urlopen(r).read()

	parseResponse(response)

if __name__ == "__main__":
	AuthXML = populateAuthXML(load(open('Input.json','r')))
	AuthRes(AuthXML)
