# This implementation of EPG takes data as XML and produces corresponding pseudonymized data

from lxml import etree
from utils import generalize_or_supress
from hashlib import sha256
from count import getLast, saveCount
import pickle
from hmac import new
from random import random
from json import loads
from bigchain import putonBlockChain, findRecord

def EPGAinit(IDPath):
	idt = open(IDPath,'rt').read()

	Qti = etree.fromstring(idt)

	print('Loading Identifiers')
	print('Quasi Specifiers..')
	print(', '.join(Qti.keys()))
	print('Applying EPGAD_Init on Qti')
	
	gQti = [generalize_or_supress(i[1],i[0]) for i in zip(Qti.keys(),Qti.values())]

	hmacKey = ""

	for i in gQti:
		hmacKey+=i

	Gi = sha256(hmacKey.encode()).hexdigest()

	countObj = getLast(Gi)
	GiObj = pickle.loads(countObj.GiObj)

	if GiObj['cQueue'].empty():
		if 'count' not in GiObj.keys():
			GiObj['count'] = 0
			count = 0
		else:
			GiObj['count']+=1
			count = GiObj['count']
		countObj.GiObj = pickle.dumps(GiObj)
		saveCount(countObj)

	prime = 179426549

	if count >= prime:
		 raise Exception('Prime Exceeded')

	else:
		res = count**2%prime
		if count <= prime/2:
			GUi = res
		else:
			GUi = prime - res

	Hi = new(Gi.encode() + str(GUi).encode() , hmacKey.encode() , sha256).hexdigest()
	return Hi, GUi


def EPGAD(ReportPath, Hi=None, GUi = None):
	if Hi == None:
		Hi = sha256(str(random()).encode()).hexdigest()
	jsn = open(ReportPath, 'rt').read()
	jsnld = loads(jsn)
	print('Report Loaded')
	print('Finding Subject Information')
	if 'subject' in jsnld.keys():
		print('Subject Information Found')
		if 'display' in jsnld['subject'].keys():
			jsnld['subject']['display'] = ""
			print('Subject Display Found and Suppressed')
		if 'reference' in jsnld['subject'].keys():
			jsnld['subject']['reference'] = Hi
			print('Replacing Identifier with ', Hi)

	print('Placing Record Asset on BlockChain')
	print()
	txid = putonBlockChain(jsnld,Hi, GUi)
	print('Status OK. Retrieving Transaction')
	findRecord(txid)

if __name__ == "__main__":
	Hi, GUi = EPGAinit('sampleIdentity.xml')
	EPGAD('sampleReport.json', Hi, GUi)
