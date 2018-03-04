from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from os import path
from sys import path as sys_path
from json import dumps
from requests import post,get

master_dir = path.abspath(path.join(__file__,'..','..','..','..'))
cli_clients = path.join(master_dir,'CLI Clients')
sys_path.append(cli_clients)

from AUA import config,OTPInit

def index(request,eid,tok):
	if request.method == "POST":
		req_mutable = request.POST.dict()
		req_mutable.pop('csrfmiddlewaretoken')
		try:
			fp = get('http://localhost:5000/get').text
		except:
			fp = 'XXXX'
		req_mutable['fp'] = fp
		req_json = dumps(req_mutable)
		response = post(config.KeyServerURL+'EnrollResident/'+req_mutable['uid']+'/',data = req_json).text
		if  response == 'true':
			return render(request,'rindex.html',{'isfail':'0'})
		else:
			return render(request,'rindex.html',{'isfail':'1'}) 
	return render(request,'rindex.html',{'isfail':'none'})

