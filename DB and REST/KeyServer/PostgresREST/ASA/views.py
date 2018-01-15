from fingerprint.views import FingerprintExists,CanSign
from json import loads,dumps
from rest_framework.views import APIView
from rest_framework.response import Response
from lxml import etree
from django.conf import settings
from os import path
from OpenSSL.crypto import load_certificate, FILETYPE_PEM
from Crypto.PublicKey import RSA
from sys import version_info
from json import loads

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

	def getCertificate(self, field, cert_path=settings.CERT_PATH):
		relpath = (path.join(path.dirname(__file__),cert_path))
		cert_raw = open(relpath,'rt').read()
		cert = load_certificate(FILETYPE_PEM, cert_raw)
		if field == "expiry":
			return cert.get_notAfter()
		elif field == "raw":
			return '\n'.join(cert_raw.split('\n')[1:-2])

	def post(self, request):
			# DRF parses the header as HTTP_X_DEVICE
		device = request.META.get('HTTP_X_DEVICE')
		ac = request.META.get('HTTP_X_AC')
		if device is None:
			# Malicious attempt
			return Response('MAL_ATTEMPT')
		else:
			if not FingerprintExists(device):
				return Response('DEVICE_NOT_REGISTERED')
			else:
				# Request is authentic, log the request for future
				# corresponding to the Fingerprint
				pass

		body = request.body
		AuthNode = etree.fromstring(body)
		uid = AuthNode.get("uid")
		ver = AuthNode.get("ver")
		URL = self.NirAadhaarURL+ver+"/"+ac+"/"+uid[0]+"/"+uid[1]+"/"+self.ASALK+"/"

		# Check if the corresponding AUA is authorized to not sign the request
		cansign = CanSign(device)

		if AuthNode.find('Signature').text is None :
			# if AuthNode doesn't have Signature of AUA then Sign it for AUA
			if cansign:
				AuthNode.find('Signature').text = self.getCertificate('raw')
				AuthNode.find('Skey').set("ci",self.getCertificate('expiry'))
				r = Request(URL,data=etree.tostring(AuthNode))
			else:
				return Response('ASA_SIGN_IS_FALSE')
		else:
			# The request is authentic and signed by AUA / Healthcenter
			pass
		r = Request(URL,data=body)
		return Response(loads(urlopen(r).read().decode('utf-8')))

class GetOTP(APIView):
	def __init__(self):
		self.NirAadhaarURL = "http://localhost:8001/"
		self.ASA = "VRAHAD"
		self.ASALK = "ASALK_TEST_KEY"

	def post(self, request):
		# DRF parses the header as HTTP_X_DEVICE
		device = request.META.get('HTTP_X_DEVICE')
		version = request.META.get('HTTP_X_API_VER')
		ac = request.META.get('HTTP_X_AC')
		uid = request.META.get('HTTP_X_UID')

		if device is None:
			# Malicious attempt
			return Response('MAL_ATTEMPT')
		else:
			if not FingerprintExists(device):
				return Response('DEVICE_NOT_REGISTERED')
			else:
				# Request is authentic, log the request for future
				# corresponding to the
				pass
		URL = self.NirAadhaarURL+'otp'+'/'+version+'/'+ac+'/'+uid[0]+'/'+uid[1]+'/'+self.ASALK+'/'
		return Response(loads(urlopen(Request(URL,data=request.body)).read()))
