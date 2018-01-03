# Verifier uses as PC Fingerprint via 0: Processor ID, 1: BaseBoard Serial, 2: System UUID

# FFF-HASH

# Create A Hash of these and send it to the postgreXL Server

import subprocess
from random import shuffle
from hmac import new
from hashlib import sha256


def linux_fingerprint():
	proc = subprocess.Popen(['sudo dmidecode'], stdout=subprocess.PIPE, shell=True)
	output = proc.communicate()[0].split(b'\n\n')
	processor = output[5]
	baseboard = output[3]
	system = output[2]
	argsList = []
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
			argsList.append(parts[1])
			break
	# Mind that we shall always have PID on 0th index, Serial Number at 1st and
	# UUID at 2nd, To make it even more random we will append a Flag indicating
	# the sequence of these arguments in computing hash
	# Indeed we dont need to specify all three. We can just specify the starting 2
	# third one is 3 - sum()
	copy = argsList[:]
	shuffle(argsList)
	flag = ""
	for i in range(len(copy)-1):
		flag += str(argsList.index(copy[i]))
	without_flag = new(key= bytes(flag,'utf-8'),msg=b''.join(argsList),digestmod=sha256)
	fingerprint = flag+without_flag.hexdigest()
	print(fingerprint)


if __name__ == "__main__":
	linux_fingerprint()
