from urllib3 import PoolManager
from json import dumps
import socket
from dmidecoder import linux_fingerprint

SPOCID = "TEST_ID"
# Password is TEST_PASS

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

def send_to_API():
	if not is_connected():
		print(bcolors.WARNING+"Please check Internet Connection."+bcolors.ENDC)
		exit(0)
	SPOCPass = input('\nPlease Enter Passphrase\n')
	# Authenticate SPOC
	while SPOCPass == '\n':
		SPOCPass = input('\nPlease Enter Passphrase\n')
	http = PoolManager()
	r = http.request('POST', 'http://localhost:8000/SPOC/',\
					headers={'Content-Type': 'application/json'},\
					body=dumps({"SPOCID":SPOCID,"pass":SPOCPass}))
	if r.data == b'true':
		r2 = http.request('POST', 'http://localhost:8000/fingerprint/',\
						headers={'Content-Type': 'application/json'},\
						body=dumps({"SPOCID":SPOCID,"fingerprint":linux_fingerprint()}))
		if r2.data == b'201':
			print(bcolors.OKGREEN+"Registration Successful."+bcolors.ENDC)
		elif r2.data == b'400':
			print("Something Went Wrong. Please Retry.")
		elif r2.data == b'405':
			print(bcolors.FAIL+"System is already registered."+bcolors.ENDC)
		else:
			print("Exiting")
	else:
		print(bcolors.FAIL+'Wrong Password. Exiting...'+bcolors.ENDC)

try:
	send_to_API()
except:
	if is_connected():
		print(bcolors.WARNING+"Server Down Please Try Again Later."+bcolors.ENDC)
