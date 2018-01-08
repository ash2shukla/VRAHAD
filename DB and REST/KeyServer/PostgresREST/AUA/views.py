from fingerprint.models import HealthCenter
from .models import LicenseKey
from json import loads,dumps

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from sys import version_info
from time import time

py_ver = version_info[0]
if py_ver == 3:
	from urllib.request import Request, urlopen
	from urllib.parse import urlencode
elif py_ver == 2:
	from urllib2 import Request, urlopen
	from urllib import urlencode

class getKey(APIView):

	def __init__(self):
		self.ASA = "VRAHAD"
		self.URL = "http://localhost:8001/getLicenseKey/"

	def prepareKey(self):
		lKey = LicenseKey.objects.all()
		if lKey:
			# If licenseKey exists then retrieve it.
			# check if it is valid
			lKey= lKey.first()
			if (int(time()) - int(lKey.ts)) < 3600:
				return lKey.lk
			else:
				lkey_from_aadhaar = loads(urlopen(Request(self.URL+self.ASA)).read().decode('utf-8'))
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
		return Response('')
