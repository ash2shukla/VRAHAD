from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from os import urandom
from hashlib import sha256
from base64 import b64encode, b64decode
from django.conf import settings

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

class EmployeeSession(APIView):
	def get(self,request,eid,tok):
		tokS = settings.HCENTER_CONN.get(eid)
		if tokS is None:
			return Response(False)

		if tokS.decode('utf-8') == tok:
			newtok = (sha256(urandom(128)).hexdigest())
			# Create a new public/private key
			private_key = ec.generate_private_key(ec.SECT571R1,default_backend())
			public_key = private_key.public_key()

			# Serialize private/public Key
			serialized_private = b64encode(private_key.private_bytes(
 				encoding=serialization.Encoding.PEM,
				format=serialization.PrivateFormat.PKCS8,
				encryption_algorithm=serialization.NoEncryption()
				))

			serialized_public = b64encode(public_key.public_bytes(
				encoding=serialization.Encoding.PEM,
				format=serialization.PublicFormat.SubjectPublicKeyInfo
				))

			settings.HCENTER_CONN.set(eid,newtok,300)
			settings.HCENTER_CONN.set(eid+"pvt",serialized_private,300)
			return Response({"tok":newtok,"pub":serialized_public})
		else:
			return Response(False)

class AuthedSessions(APIView):
	def get(self,request,eid,tok):
		# eid+"auth" contains TXNID
		# eid+"authed" contains last Authed Token
		# if eid+"auth" is None - Employee didn't authenticate Biometrics
		txnS = settings.HCENTER_CONN.get(eid+"auth")
		if txnS is None:
			return Response(False)

		tokS = settings.HCENTER_CONN.get(eid+"authed")
		if tokS.decode('utf-8') != tok:
			return Response(False)

		newtok = (sha256(urandom(128)).hexdigest())
		# Create a new public/private key
		private_key = ec.generate_private_key(ec.SECT571R1,default_backend())
		public_key = private_key.public_key()

		# Serialize private/public Key
		serialized_private = b64encode(private_key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.NoEncryption()
			))

		serialized_public = b64encode(public_key.public_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PublicFormat.SubjectPublicKeyInfo
			))

		settings.HCENTER_CONN.set(eid,newtok,300)
		settings.HCENTER_CONN.set(eid+"pvt",serialized_private,300)
		return Response({"tok":newtok,"pub":serialized_public})
