from flask import Flask
from bs4 import BeautifulSoup
from requests import get
from json import dumps
url = "https://www.receive-sms-online.info/919654766051-India"

app = Flask(__name__)

isVrahadSMS = lambda x: True if len(x.split(',')) == 3 and len(x.split())==1 else False

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
	return dumps(res if res != {} else '')

if __name__ == '__main__':
	app.run()
