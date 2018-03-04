from flask import Flask
from flask import request
from flask import Response
from json import loads
from queue import Queue

q = ['XXXX']

app = Flask(__name__)

@app.route('/',methods=['POST'])
def method():
	dic = loads(request.data.decode('utf-8'))
	q[0] = list(dic.values())[0]
	return 'Logged'

@app.route('/get',methods=['GET'])
def getmethod():
	resp = Response(q[0])
	resp.headers['Access-Control-Allow-Origin'] = '*'
	q[0] = 'XXXX'
	return resp

if __name__ == '__main__':
	app.run(host='0.0.0.0')
