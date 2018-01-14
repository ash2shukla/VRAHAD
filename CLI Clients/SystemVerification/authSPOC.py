from json import dumps
import socket
from dmidecoder import linux_fingerprint
from sys import version_info

base_URL = "localhost"

py_ver = version_info[0]
if py_ver == 3:
	from urllib.request import Request, urlopen
	input_stream = input
elif py_ver == 2:
	from urllib2 import Request, urlopen
	input_stream = raw_input

SPOCID = "TEST_ID"
# Password is TEST_PASS, Hash = 4aa82e9758818da6d4b62fe8d485749a

class bcolors:
	# For Colored Console I/O
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def is_connected():
	try:
		socket.create_connection(("www.google.com", 80))
		return True
	except OSError:
		pass
	return False

def to_bytes(string):
	if py_ver == 3:
		return bytes(string,'utf-8')
	elif py_ver == 2:
		return bytes(string)

def open_url(type,url,body):
	q = Request(url,data = to_bytes(body))
	q.add_header('Content-Type','application/json')
	return urlopen(q).read()

def send_to_API():
	if not is_connected():
		print(bcolors.WARNING+"Please check Internet Connection."+bcolors.ENDC)
		exit(0)
	SPOCPass = input_stream('\nPlease Enter Passphrase\n')
	# Authenticate SPOC
	while SPOCPass == '\n':
		SPOCPass = input_stream('\nPlease Enter Passphrase\n')
	SPOCAuth = open_url('POST','http://'+base_URL+':8000/SPOC/',dumps({"SPOCID":SPOCID,\
					"pass":SPOCPass}))

	if SPOCAuth == b'true':
		print('Please Wait...')
		InsertCode = open_url('POST', 'http://'+base_URL+':8000/fingerprint/'\
						,dumps({"SPOCID":SPOCID,"fingerprint":linux_fingerprint()}))
		if InsertCode == b'201':
			print(bcolors.OKGREEN+"Registration Successful."+bcolors.ENDC)
		elif InsertCode == b'400':
			print("Something Went Wrong. Please Retry.")
		elif InsertCode == b'405':
			print(bcolors.FAIL+"System is already registered."+bcolors.ENDC)
		else:
			print(InsertCode)
	else:
		print(bcolors.FAIL+'Wrong Password. Exiting...'+bcolors.ENDC)

try:
	send_to_API()
except:
	if is_connected():
		print(bcolors.WARNING+"Server Down Please Try Again Later."+bcolors.ENDC)
