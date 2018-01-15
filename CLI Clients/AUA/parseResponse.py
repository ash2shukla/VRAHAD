from json import loads
from lxml import etree
def parseResponse(arg):
	'''
	Parses the Response and raises Exceptions baesd on the Response Codes.
	'''
	print(loads(arg))
