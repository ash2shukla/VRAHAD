from sys import path as sys_path
from os import path

master_dir = path.abspath(path.join(__file__,'..','..'))
sys_path.append(master_dir)

from SystemVerification.dmidecoder import linux_fingerprint

device = linux_fingerprint()

NirAadhaarURL = "http://localhost:8001/"
KeyServerURL = "http://localhost:8000/"
PublicKeyPath = "TEST_CENTER.public.pem"
CertPath = "TEST_CENTER-AUA_CERT/TEST_CENTER-AUA-USER.cert.pem"

ver = "1.6"
ac = "TEST_CENTER" 	# auaID
sa = "VRAHAD" # sa = ac as we don't have subdivisons'
aua = "TEST_CENTER"
is_Fingerprint = True
is_Iris = True
lot = "G" 		# can also set it to P
ki = ""			# OtherDocuments/DigitalCertificates_ for other info
dtype="X"
is_otp =False
is_pin = False
is_asa_cert= False
tkntype= ""
tknvalue = ""
lot = "G"

############################# VARIABLES FOR EKYC ##############################

ekyc_ver = "2.0"
ra = "FI" # F,I,O,P Fingerprint, Iris, OTP and Pin
			# IT MUST MATCH WITH PID Uses block
rc = "Y" # resident's consent can only be Y
mec = "Y" # get mobile and email's consent
lr = "N" # Get Local Reigional Language Data
de = "Y" # Y = KUA/AUA encrypts N = KSA/ASA encrypts
pfr = "N" # Print format Request (Returns a PDF as well)
