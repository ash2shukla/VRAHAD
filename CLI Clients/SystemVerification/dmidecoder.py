#!/usr/bin/env python

# Create a Fingerprint using Processor ID, BaseBoard Serial, System UUID

import subprocess
from hmac import new
from string import ascii_uppercase,digits
from hashlib import sha256
from random import random
# Such ID will be embedded inside application at each download the application
# CAN BE COMPILED with this information from whatever account SPOC has logged in
# So that it's unique to each SPOC
def randomAlnum(length):
	num = len(ascii_uppercase+digits)
	retval = ""
	for i in range(length):
		retval+=((ascii_uppercase+digits)[(int(random()*100)%(num))])
	return retval

def linux_fingerprint():
	proc = subprocess.Popen(['sudo dmidecode'], stdout=subprocess.PIPE, shell=True)
	output = proc.communicate()[0].split(b'\n\n')
	processor = output[5]
	baseboard = output[3]
	system = output[2]
	argsList = []
	key = b"default"

	for i in processor.split(b'\n\t'):
		parts = i.split(b': ')
		if parts[0] == b"ID":
			argsList.append(parts[1])
			break

	for i in baseboard.split(b'\n\t'):
		parts = i.split(b': ')
		if parts[0]==b"Serial Number":
			argsList.append(parts[1])
			break

	for i in system.split(b'\n\t'):
		parts = i.split(b': ')
		if parts[0] == b"UUID":
			key = parts[1]
			break

	fingerprint = new(key= key,msg=b''.join(argsList),digestmod=sha256).hexdigest()

	# Someone can guess that we are calculating a sha256 hash using two criterias
	# 1st, length of correspdoning hex is 256 bit (Add a random 5 letter string in front of it)
	# which we won't consider while matching the fingerprint
	# 2nd, all used chars are a-zA-Z0-9 replace 0,1,2 with @ % and #

	fingerprint = randomAlnum(5)+\
				fingerprint.replace('0','@').replace('1','!').replace('2','$')
	return fingerprint
