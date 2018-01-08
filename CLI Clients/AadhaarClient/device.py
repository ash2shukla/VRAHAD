# Device returns Terminal ID , device would have it already embedded
# it would return the same on calling getTID function

def getTID(**kwargs):
	# Implement any logic for verifying the request
	return "TEST_TID"

def getUDC(**kwargs):
	# Realtek [vid]= XXXX (4 digits num)
	# date of deployment = "111111" (6 digits num)
	# serial = XXXXXXXXXX ( 10 digits alnum)
	return "XXXX111111XXXXXXXXXX"
