from json import loads
def parseResponse(arg):
	'''
	Parses the Response and raises Exceptions baesd on the Response Codes.
	'''
	print(loads(arg))
