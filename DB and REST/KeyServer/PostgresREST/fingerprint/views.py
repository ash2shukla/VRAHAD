from .models import Fingerprint,HCenterSPOC
from .serializers import FingerprintSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hmac import new

def FingerprintExists(fprint):
	return Fingerprint.objects.filter(fingerprint__endswith=fprint[5:]).exists()

def CanSign(fprint):
	Fobj = Fingerprint.objects.get(fingerprint__endswith=fprint[5:])
	return Fobj.SPOCID.HealthCenter.Data['asa_sign']

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
		print(request.data)
		if not Fingerprint.objects.filter(fingerprint__endswith=request.data['fingerprint'][5:]).exists():
			# serializer = FingerprintSerializer(data={'SPOCID':HCenterSPOC.objects.get(\
			# 									SPOCID=request.data['SPOCID']),\
			# 									'fingerprint':request.data['fingerprint']})
			serializer = FingerprintSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(status.HTTP_201_CREATED)
			return Response(status.HTTP_400_BAD_REQUEST)
		else:
			return Response(status.HTTP_405_METHOD_NOT_ALLOWED)


class HCenterSPOCVerify(APIView):
	"""
	Authenticate HCenterSPOC
	"""
	def post(self,request,format=None):
		# Verify that the password is same
		data = request.data
		SPOCID = data['SPOCID']
		Pass = new(bytes(SPOCID,'utf-8'),bytes(data['pass'],'utf-8')).hexdigest()
		if HCenterSPOC.objects.filter(SPOCID=SPOCID,passhash=Pass).exists():
			return Response(True)
		else:
			return Response(False)
