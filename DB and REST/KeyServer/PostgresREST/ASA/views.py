from fingerprint.models import HealthCenter
from json import loads,dumps

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lxml import etree

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

class ForwardAuthReq(APIView):
	'''
	Forwards Authentication request of ASAs to Aadhaar Server
	Returns the response of Aadhaar Server to ASA
	'''
	def __init__(self):
		self.NirAadhaarURL = "http://localhost:8001/"
		self.ASA = "VRAHAD"
		self.ASALK = "ASALK_TEST_KEY"
	def post(self,request):
		try:
			body = request.body
			AuthNode = etree.fromstring(body)
			uid = AuthNode.get("uid")
			ver = AuthNode.get("ver")
			URL = self.NirAadhaarURL+ver+"/"+self.ASA+"/"+uid[0]+"/"+uid[1]+"/"+self.ASALK
			r = Request(URL,data=body)
			return Response(urlopen(r).read())
		except:
			# Improper XML
			return Response("BAD_XML")
