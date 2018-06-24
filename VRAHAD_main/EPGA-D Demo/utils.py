from re import match,split
from calendar import month_name, month_abbr
from PyZIPIN import encode

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
	gen_attrib = ['yob','pc','gender']
	if atype is not None:
		if atype in gen_attrib:
			return attrib
		else:
			return ''
	else:
		# Suppress the value
		return ''

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
