from re import match,split
from calendar import month_name, month_abbr
from PyZIPIN import encode
from bs4 import BeautifulSoup as BS

month_name = [i.lower() for i in month_name]
month_abbr = [i.lower() for i in month_abbr]

def generalize_or_supress(attrib,atype=None):
	# if atype is None then try to guess the type of attribute based on bag of words model
	# Checking sequence is
	# isGender
	# isName
	# isDOB
	# isPlace
	# isAddress
	# isYOB
	# isUID
	gen_attrib = ['dob','pc','gender']
	Poa = attrib.find('Uid').find('Poa')
	Poi = attrib.find('Uid').find('Poi')
	ret = []
	for i,j in zip(Poi.keys(), Poi.values()):
		if i in gen_attrib:
			if i == 'dob':
				ret.append(j.split('-')[0])
			else:
				ret.append(j)
	for i,j in zip(Poa.keys(), Poa.values()):
		if i in gen_attrib:
				ret.append(j)
	return ret
	
	

def isName(arg):
	m = match(r'([A-Z][a-z][a-z]*)\s*([A-Z][a-z]*.?)*\s*([A-Z][a-z][a-z][a-z]*)',arg)
	if m is None:
		return False
	else:
		return any(i is not None for i in m.groups())

def isYOB(arg):
	try:
		int(arg)
	except:
		return False
	if len(arg) == 4:
		if int(arg)-1850>0:
			return True
	return False

def isPlace(arg):
	parts = split(r'[,\-\\/]\s*', arg,maxsplit=2)
	if len(parts) >1:
		return False

	if parts is not None:
		return True
	else:
		return False

def isUID(arg):
	if len(arg) != 12:
		return False
	try:
		int(arg)
		return True
	except:
		return False

def isGender(arg):
	arg = arg.lower()
	if arg in ['male','female','transgender','other']:
		return True
	elif len(arg)==1:
		if arg in ['m','f','o']:
			return True
		else:
			return False
	return False

def isDOB(arg):
	parts = split(r'[,\-\\/]\s*', arg,maxsplit=2)
	if len(parts) == 3:
		# might be date
		# check the length of each one part should be 4 other 2,2
		# if num if al then lower must belong to month_name or month_abbr
		len_parts = [len(i) for i in parts]
		try:
			idx4 = len_parts.index(4)
		except ValueError:
			return False
		if int(parts[idx4])-1850 >0:
			# Year exists check other
			if parts[(idx4+1)%3].isalpha():

				if parts[(idx4+1)%3].lower() in month_name+month_abbr:
					return parts[idx4]
				else:
					return False
			elif len(parts[(idx4+1)%3]) == 2:
				try:
					int(parts[(idx4+1)%3])
				except:
					return False

			if parts[(idx4-1)%3].isalpha():
				if parts[(idx4-1)%3].lower() in month_name+month_abbr:
					return parts[idx4]
				else:
					return False
			elif len(parts[(idx4-1)%3]) == 2:
				try:
					int(parts[(idx4-1)%3])
					return parts[idx4]
				except:
					return False
		else:
			return False
	else:
		return False

from urllib.request import HTTPCookieProcessor,build_opener
from http.cookiejar import CookieJar

def sendSMSto(to_number,gui):
		url ='http://site24.way2sms.com/Login1.action?'
		data = bytes('username=9818611161&password=123ashish&Submit=Sign+in','utf-8')
		# 7988367320
		cj= CookieJar()
		opener = build_opener(HTTPCookieProcessor(cj))
		opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
		try:
			opener.open(url, data)
		except IOError:
			return "ERR: SENDMSG"

		jession_id =str(cj).split('~')[1].split(' ')[0]
		send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
		send_sms_data = bytes('ssaction=ss&Token='+jession_id+'&mobile='+to_number+'&message='+'Your GUID is '+gui+'&msgLen=136','utf-8')
		print('SENT OTP IS',gui)
		opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
		try:
			sms_sent_page = opener.open(send_sms_url,send_sms_data)
			soup = BS(sms_sent_page.read())
			errNode = soup.find('span',{'class':'err'})
			if errNode:
				print(errNode)
				return "ERR: SENDMSG"
			else:
				return "SUCCESS: SENDMSG"
		except IOError:
			return "ERR: SENDMSG"
		return "SUCCESS: SENDMSG"