from .models import Fingerprint,HCenterSPOC, HCenterEmployee, GIDMap, RecordMaps
from .serializers import FingerprintSerializer
from django.http import Http404, HttpResponse
from base64 import b64encode, b64decode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hmac import new
from json import loads
from django.conf import settings
from os import urandom
from hashlib import sha256
from sys import path as sys_path
from os import path,urandom
from lxml import etree
from .utils import generalize_or_supress, sendSMSto

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from Crypto.Cipher import AES
from Crypto import Random

master_dir = path.abspath(path.join(__file__,'..','..','..','..','..'))
cli_clients = path.join(master_dir,'CLI Clients')
sys_path.append(cli_clients)

from AUA import config,OTPInit,AuthInit,eKYCInit

def nothing(request):
	res = HttpResponse('')
	res['Access-Control-Allow-Origin'] = '*'
	return res

def FingerprintExists(fprint):
	idx = int(fprint[-1])
	fprint = fprint[:idx]+fprint[idx+5:-1]
	return Fingerprint.objects.filter(fingerprint__exact=fprint).exists()

def CanSign(fprint):
	idx = int(fprint[-1])
	fprint = fprint[:idx]+fprint[idx+5:-1]
	Fobj = Fingerprint.objects.get(fingerprint__exact=fprint)
	return Fobj.SPOCID.HealthCenter.Data['asa_sign']

def getLast(gi):
	try:
		giObject = GIDMap.objects.get(gi = gi)
		if giObject.cQueue:
			count = giObject.cQueue.pop()
		else:
			count = giObject.count
			giObject.count+=1
		giObject.save()
		return count
	except:
		GIDMap(gi=gi,count=1).save()
		return 1

def randomize_count(count):
	count = int(count)
	prime = 179426549

	if count >= prime:
		 raise Exception('Prime Exceeded')
	else:
		res = (count**2)%prime
		if count <= prime/2:
			gui = prime-res
		else:
			gui = res
	return str(gui)

def EPGA_Init(Qti):
	gQti = generalize_or_supress(Qti)
	kGi = ''
	kGi = ''.join(gQti)
	gi = sha256(kGi.encode()).hexdigest()
	count = getLast(gi)
	gui = randomize_count(count)
	Hi = new(kGi.encode(),(gi+gui).encode(),sha256).hexdigest()
	RecordMaps(HealthID=Hi).save()
	return str(gui)

class FingerprintVerify(APIView):
	"""
	Verify a Fingerprint return Boolean for Authentication.
	"""
	def get(self, request, fp, format=None):
		if Fingerprint.objects.filter(fingerprint=fp).exists():
			return Response(True)
		else:
			# Write a logic to blacklist IP
			return Response(False)

class FingerprintSave(APIView):
	"""
	Save a Fingerprint.
	"""
	def post(self, request,format=None):
		# Check if fingerprint exists
		fingerprint_full = request.data['fingerprint']
		idx = int(fingerprint_full[-1])
		request_fingerprint = fingerprint_full[:idx]+fingerprint_full[idx+5:-1]
		request.data['fingerprint'] = request_fingerprint

		if not Fingerprint.objects.filter(fingerprint__exact=request_fingerprint).exists():
			# If Fingerprint doesn't exist then create a ECC key pair and return the public key in response
			SPOCID = request.data['SPOCID']
			if settings.REDIS_CONN.get(SPOCID).decode('utf-8') == request.data.pop('tok'):
				serializer = FingerprintSerializer(data=request.data)
				if serializer.is_valid():
					serializer.save()
					return Response(status.HTTP_201_CREATED)
				else:
					return Response(status.HTTP_400_BAD_REQUEST)
			else:
				return Response(status.HTTP_400_BAD_REQUEST)
		else:
			return Response(status.HTTP_405_METHOD_NOT_ALLOWED)


class HCenterSPOCVerify(APIView):
	"""
	Authenticate HCenterSPOC and returns a token.
	"""
	def post(self,request,format=None):
		# Verify that the password is same
		data = request.data
		SPOCID = data['SPOCID']
		Pass = new(bytes(SPOCID,'utf-8'),bytes(data['pass'],'utf-8')).hexdigest()
		if HCenterSPOC.objects.filter(SPOCID=SPOCID,passhash=Pass).exists():
			# Create a token in SPOCID in REDIS_CONN for 30 seconds
			tok = sha256(urandom(128)).hexdigest()
			settings.REDIS_CONN.set(SPOCID, tok, 30)
			return Response(tok)
		else:
			return Response(False)

class HCenterEmployeeVerify(APIView):
	"""
	Verify HCenterEmployee by his uname and pass.
	"""
	def post(self,request,format=None):
		# Verify that the employee ID exists
		EID = request.data['EID']
		Pass = new(bytes(EID,'utf-8'),bytes(request.data['pass'],'utf-8')).hexdigest()

		if HCenterEmployee.objects.filter(EmployeeID=EID).exists():
			EmpObj = HCenterEmployee.objects.get(EmployeeID=EID)
			if EmpObj.Data['passhash'] == Pass:
				# Generate a Session Token for Employee and return it
				# Hash a random number
				if OTPInit('10',EmpObj.Data['UID']).get('code') == 'OK':
					tok = sha256(urandom(128)).hexdigest()
					settings.REDIS_CONN.set(EID,tok,300)
					return Response(tok)
		return Response(False)

class HCenterEmployeeAuth(APIView):
	def DecAES(self,key,textbytes):
		iv = key[:AES.block_size]
		cipher = AES.new(key, AES.MODE_CBC, iv)
		decrypted = cipher.decrypt(textbytes)[len(iv):]
		return decrypted.decode('utf-8').split('"}')[0]+'"}'

	def post(self,request,eid,tok,format=None):
		# Verify that the employee ID exists
		tokR = settings.REDIS_CONN.get(eid)
		if tokR is None:
			return Response(False)
		#  TokR is not None
		if not isinstance(tokR,bytes):
			return Response(False)

		# TokR is a bytes buffer
		if tokR.decode('utf-8') == tok:
			request = loads(request.body)
			salt = b64decode(tok)
			EncData = b64decode(request['data'])

			loaded_public_key = serialization.load_pem_public_key(
				b64decode(request['pub']),
				backend=default_backend()
			)

			loaded_private_key = serialization.load_pem_private_key(
				b64decode(settings.REDIS_CONN.get(eid+"pvt")),
				# or password=None, if in plain text
				password=None,
				backend=default_backend()
			)

			shared_key = loaded_private_key.exchange(ec.ECDH(), loaded_public_key)

			kdf = PBKDF2HMAC(
				algorithm=hashes.SHA256(),
				length=32,
				salt=salt,
				iterations=100000,
				backend=default_backend()
			)

			AESkey = kdf.derive(shared_key)

			DecData = self.DecAES(AESkey, EncData)
			DecDataJSON = loads(DecData)
			OTP = DecDataJSON['OTP']
			if HCenterEmployee.objects.filter(EmployeeID=eid).exists():
				EmpObj = HCenterEmployee.objects.get(EmployeeID=eid)
					# Generate a Session Token for Employee and return it
					# Hash a random number
				config.InputTemplate['uid'] = EmpObj.Data['UID']
				config.InputTemplate["bio_dict"]["FMR"] = {"LEFT_THUMB":DecDataJSON["BIO"]}
				res= AuthInit(config.InputTemplate, OTP)
				if res.get('actn') == "RETRY":
					res = AuthInit(config.InputTemplate, OTP)
				if res.get('ret') == "Y":
					# Employee Verification complete
					# In redis save EID + "auth" = Txn ID of AuthInit response
					settings.REDIS_CONN.set(eid+"auth",res.get('txn'),10*3600) # Valid for 10 hours.
					# Create a new token Encrypt it with the AESkey and return in response a newcreated Token
					# From this point on after recieving this token HealthCenter will request Sessions from Auth Channel
					# from Session Server
					tok = sha256(urandom(128)).hexdigest()
					settings.REDIS_CONN.set(eid+"authed",tok,3600) # One Token is valid for One Hour.
					return Response(tok)
				else:
					return Response(False)
		return Response(False)

class EnrollResident(APIView):
	def post(self,request,uid):
		data = loads(request.body)
		uid = data['uid']
		fp = data['fp']
		otp = data['otp']
		config.InputTemplate['uid'] = uid
		config.InputTemplate["bio_dict"]["FMR"] = {"LEFT_THUMB":fp}
		res= eKYCInit(config.InputTemplate,otp)
		if res.get('actn') == "RETRY":
			res = eKYCInit(config.InputTemplate, OTP)
		if res.get('ret') == "Y":
			gui = EPGA_Init(res)
			try:
				to = res.find('Uid').find('Poi').get('phone')[2:]
				sendSMSto(to,gui)
				return Response(True)
			except:
				return Response(False)
		return Response(False)

	def get(self,request,uid):
		otp = OTPInit(uid=uid,ch='10')
		if otp.get('ret')=='Y':
			res = Response('OTP Generated, Scan Thumb Please.',headers={'Access-Control-Allow-Origin':'*'})
		else:
			res = Response('Could Not Generate OTP',headers={'Access-Control-Allow-Origin':'*'})
		return res
