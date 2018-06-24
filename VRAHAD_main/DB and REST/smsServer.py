from flask import Flask,Response
from bs4 import BeautifulSoup
from requests import get
from json import dumps
url = "https://www.receive-sms-online.info/919654766051-India"

app = Flask(__name__)

isVrahadSMS = lambda x: True if x.split()[-1]=="GISBDSM" else False

@app.route('/')
def index():
	bs = BeautifulSoup(get(url).text)
	res = []
	for i,j in zip(bs.findAll('td',{'data-label':'From   :'}),bs.findAll('td',{'data-label':'Message:'})):
		if j.string is not None and isVrahadSMS(j.string):
			res_one = {}
			res_one['from'] = i.string
			res_one['body'] = j.string
			res.append(res_one)
	response = Response(dumps(res if res != {} else ''))
	response.headers['Access-Control-Allow-Origin']='*'
	return response

if __name__ == '__main__':
	app.run()
