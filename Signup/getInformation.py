from lxml import etree

def scanAadhaar():
	'''
	some logic to scan aadhaar card using xyz scanner device goes here
	this function must emit the scanned XML of barcode

	till actual functionality is implemented it returns the sample response through SampleScannedData
	'''

	return open('SampleScannedData','rb').read()

def getUID(xmlBytes):
	aadhaarNode = etree.fromstring(xmlBytes)
	# return uid only and verify with OTP
	uid = aadhaarNode.get('uid')
	return uid
