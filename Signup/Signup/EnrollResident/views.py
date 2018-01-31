from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from os import path
from sys import path as sys_path

master_dir = path.abspath(path.join(__file__,'..','..','..','..','..'))
cli_clients = path.join(master_dir,'CLI Clients')
sys_path.append(cli_clients)

from AUA import config

def index(request,eid,tok):
	# Check if the token is correct
	url = config.SessionServerURL+
	return HttpResponse('Resident Enrollment Logic Goes Here.')
