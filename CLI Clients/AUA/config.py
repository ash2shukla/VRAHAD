from sys import path as sys_path
from os import path
from json import load

master_dir = path.abspath(path.join(__file__,'..','..'))
sys_path.append(master_dir)

from SystemVerification.dmidecoder import linux_fingerprint

device = linux_fingerprint() # To verify the request using Fingerprint on VRAHAD ASA

SessionServerURL = "http://localhost:8002/" # Session Server port 
NirAadhaarURL = "http://localhost:8001/" # NirAadhaar's port
KeyServerURL = "http://localhost:8000/" # ASA's URL
PublicKeyPath = path.abspath(path.join(__file__,'..',"TEST_CENTER.public.pem")) # Public Key provided by NirAadhaar
CertPath = path.abspath(path.join(__file__,'..',"TEST_CENTER-AUA_CERT/TEST_CENTER-AUA-USER.cert.pem")) # Digital Certificate Path
DBPath = path.abspath(path.join(__file__,'..','lkd.db')) # LicenseKey Database Path (Should not be changed unless you're sure what you are doing)
DemoData = load(open(path.abspath(path.join(__file__,'..','Input.json')))) # A Demo input of registered user's values
InputTemplate = load(open(path.abspath(path.join(__file__,'..','Input_Template.json')))) # An Input template. Shove in values in this template.

ver = "1.6" # Version of API , only acceptable value is 1.6
ac = "TEST_CENTER" 	# AC = AUA
sa = "VRAHAD" # SA = ASA , for now Sub ASA not supported
aua = "TEST_CENTER" # HealthCenter / AUA's name goes here
is_Fingerprint = True # Set to False if not using Fingerprint Identification
is_Iris = True # Set to False if not using Iris Identification
lot = "G" 		# can also set it to P
ki = ""			# OtherDocuments/DigitalCertificates_ for other info
dtype="X"	# For now only XML is supported, Acceptable value is "P" as well in Aadhaar but not implemented yet.
is_otp =True # Set True if you want to verify using OTP as well
is_pin = False # DO NOT SET TRUE, PIN HAS NO MEANINGS, ITS FOR INTERNAL PURPOSES OF CIDR ONLY
is_asa_cert= False # DO NOT SET TRUE, ASA WONT SIGN INSTEAD OF AUA
tkntype= "" # Token usage is ambiguous and not documented thus not implemented in NirAadhaar for now.
tknvalue = "" # Same applies for Token Value

############################# VARIABLES FOR EKYC ##############################

ekyc_ver = "2.0" # Version of eKYC, only acceptable value is 2.0
ra = "FI" # F,I,O,P Fingerprint, Iris, OTP and Pin
			# IT MUST MATCH WITH PID Uses block
rc = "Y" # resident's consent can only be Y
mec = "Y" # get mobile and email's consent
lr = "N" # Get Local Reigional Language Data
de = "Y" # Y = KUA/AUA encrypts N = KSA/ASA encrypts
pfr = "N" # Print format Request (Returns a PDF as well)
