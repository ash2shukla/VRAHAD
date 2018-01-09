from fingerprint.models import HealthCenter
from .models import LicenseKey
from json import loads,dumps

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Crypto.PublicKey import RSA

from sys import version_info
from time import time
from base64 import b64encode

py_ver = version_info[0]
if py_ver == 3:
	from urllib.request import Request, urlopen
	from urllib.parse import urlencode
elif py_ver == 2:
	from urllib2 import Request, urlopen
	from urllib import urlencode

class getKey(APIView):

	def __init__(self):
		self.AUA = "VRAHAD"
		self.URL = "http://localhost:8001/getLicenseKey/"

	def prepareKey(self):
		'''
		Retrieve a LicenseKey from aadhaar and send it to the ASA.
		'''
		lKey = LicenseKey.objects.all()
		if lKey:
			# If licenseKey exists then retrieve it.
			# check if it is valid
			lKey= lKey.first()
			if (int(time()) - int(lKey.ts)) < 3600:
				return lKey.lk
			else:
				lkey_from_aadhaar = loads(urlopen(Request(self.URL+self.AUA)).read().decode('utf-8'))
				lKey.ts = int(time())
				lKey.lk = lkey_from_aadhaar
				lKey.save()
				return lkey_from_aadhaar
		else:
			# If licenseKey does not exist then retrieve it from aadhaar server
			# and save it in DB and return it
			lkey_from_aadhaar = loads(urlopen(Request(self.URL+self.ASA)).read().decode('utf-8'))
			LicenseKey(lk = lkey_from_aadhaar , ts=int(time())).save()
			return lkey_from_aadhaar

	# returns the LicenseKey fetched from Aadhaar servers encrypted with the asalk
	def get(self,request,asaID):
		# See if asaID is registered
		if HealthCenter.objects.filter(HealthCenterID__exact=asaID).exists() :
			return Response(self.prepareKey())
		# asaID i.e. HealthCenterID does not exist
		return Response('NA_ASA')

class getSession(APIView):
	'''
	Returns the encrypted session key.
	We certainly don't want to share the 2048 bit key provided by UIDAI
	'''

	# We are assuming the key to be the following key
	# generated RSA.generate(2048).publickey().exportKey()

	# The corresponding PrivateKey ie. RSA.generate(2048).exportKey()
	# is stored in AadhaarDB in AUA table as privateKey attribute

	def __init__(self):
		self.UIDAI_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmMQWV3320E2w93BCVm36\nOSrNpCsCclz5ggymWzZQeeYrPnQiEIrx4RKftVh+G6W7B4RXlQ6dUo3gY7ra5EYE\npeqdz1c4UT3jpBthYLtjftEiILeOsR2V/vX0x9CdkxfrTYETyY/Spr9ow8nqWQq+\nF0UykHGAteolLTPCSKQ1Ks4YgVsojKZ8Vo9T9PknHGkyGqWY9x1wS18oJ08gSRI/\nzTxz084cwGp+DcgGmXtri4pamNpw3nyS71Roz/G0OIag6nE4lh/eEEMnOY3rgQFq\nbFa1e5hKMfG424jwtipQx+IJ6aPbhK/2fc2vqAlh7tcUShGjaLJPxCONrYu4v2i9\n9wIDAQAB\n-----END PUBLIC KEY-----'

	def post(self,request,asaID):
		# See if asaID requesting is registerd
		print(request.data)
		if HealthCenter.objects.filter(HealthCenterID__exact=asaID).exists():
			try:
				SessionID= request.data['SessionID']
			except KeyError:
				SessionID = None

			if SessionID is not None:
				return Response(b64encode(\
							RSA.importKey(self.UIDAI_key).encrypt(bytes(SessionID,'utf-8'),32)[0]))
			else:
				return Response('No Session ID')
		else:
			return Response('asaID doesnt exist')
