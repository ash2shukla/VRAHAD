from django.shortcuts import render,redirect
from sys import path as sys_path
from json import dumps,loads
from os import path
from urllib.request import urlopen,Request
from base64 import b64decode, b64encode
from requests import get

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from Crypto.Cipher import AES
from Crypto import Random

master_dir = path.abspath(path.join(__file__,'..','..','..'))
cli_clients = path.join(master_dir,'CLI Clients')
sys_path.append(cli_clients)

from AUA import config

def EncAES(keybytes, text):
	if not isinstance(text, bytes):
		text = bytes(text, 'utf-8')
	padded = text + bytes((32 - len(text) % 32) * chr(32 - len(text) % 32),'utf-8')
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(keybytes, AES.MODE_CBC, iv)
	return b64encode(iv + cipher.encrypt(padded)).decode('utf-8')

def EncData(key, salt,data):
	"""
	key : Key received from SessionServer
	salt : Decoded Token
	data : Data to Encrypt (must be string)
	"""
	loaded_public_key = serialization.load_pem_public_key(
		key,
		backend=default_backend()
	)

	private_key = ec.generate_private_key(ec.SECT571R1,default_backend())
	shared_key = private_key.exchange(ec.ECDH(), loaded_public_key)

	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)

	# We will send the serialized public key to server for ECDHE
	serialized_public = b64encode(private_key.public_key().public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
	)).decode('utf-8')

	AESkey = kdf.derive(shared_key)

	return bytes(dumps({"pub":serialized_public,"data":EncAES(AESkey, data)}),'utf-8')


def index(request):
	if request.method == "POST":
		EID = request.POST.get('EID')
		Pass = request.POST.get('pass')
		# Send EID and pass to KeyServer and Recieve a token
		r = Request(config.KeyServerURL+"EMP/",bytes(dumps({'EID':EID,'pass':Pass}),'utf-8'))
		r.add_header('Content-Type','application/json')
		tok = loads(urlopen(r).read().decode('utf-8'))
		if tok != False:
			return redirect('/OTP/'+EID+'/'+tok)
		else:
			return render(request,'index.html',{'isfail':'1'})
	return render(request,'index.html',{'isfail':'0'})

def OTP(request,eid,tok):
	# Check if tok is authed else redirect back to index
	if request.method == "GET":
		r = Request(config.SessionServerURL+'EMPSession/'+eid+'/'+tok)
		Response = loads(urlopen(r).read().decode('utf-8'))
		if Response != False:
			return render(request,'GiveOTP.html',{'tok':Response['tok'],'k':Response['pub']})
		else:
			return redirect('/')

	elif request.method == "POST":
		keyRaw = request.POST.get('k')
		if keyRaw is None:
			return redirect('/')
		key = b64decode(keyRaw)
		tok = request.POST.get('tok')

		salt = b64decode(tok)
		# create a public/private key pair
		OTP = request.POST.get('OTP')
		try:
			Fprint = get("http://localhost:5000/get").text
		except:
			Fprint = 'XXXX'
		if OTP is not None:
			data = EncData(key,salt,dumps({"OTP":str(OTP),"BIO":Fprint}))
			r = Request(config.KeyServerURL+'EMPAuth/'+eid+'/'+tok+'/',data=data)
			tok = loads(urlopen(r).read().decode('utf-8'))
			# Forward to choose Enrollment Type page
			if tok == False:
				return redirect('/')
			return redirect('/Resident/'+eid+'/'+tok+'/')
		return redirect('/')
