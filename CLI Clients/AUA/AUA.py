from sys import version_info
from sys import path as sys_path
from json import dumps,loads,load
from time import time
from
from os import path
from lxml import etree
from hashlib import sha256
from datetime import datetime
from prepareRequest import populateAuthXML, AuthRes


master_dir = path.abspath(path.join(__file__,'..','..'))
sys_path.append(master_dir)

from SystemVerification.dmidecoder import linux_fingerprint
from urllib.request import Request, urlopen
from urllib.parse import urlencode


config = load(open('config.json'))

AadhaarURL = config['NirAadhaarURL']
KeyServerURL = config['KeyServerURL']

def AuthInit(JSONInfo):
	AuthXML = populateAuthXML(JSONInfo)
	AuthRes(AuthXML)

def OTPInit(is_otp,ch):
	device =  linux_fingerprint()
	ver = "1.6"
	ac = "TEST_CENTER"
	sa = "VRAHAD"
	getOTP(is_otp,ver,ac,uid,device,sa,ch)

def eKYCInit():
	pass


if __name__ == "__main__":
	AuthInit(load(open('Input.json','r')))
