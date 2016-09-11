from flask import Flask
from flaskext.mysql import MySQL
import requests
from pprint import pprint
import json
from os import listdir, walk
import time

def checkFile():
	prefix = time.strftime('%Y_%m_%d')
	exit = False
	for filename in listdir('./files'):
		if filename == prefix:
			exit = True
			break;
	if exit == False:
		f = open('./files/'+prefix, 'w')
		return f


def init():
	s_list = ['GOOG', 'AAPL']
	url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22YHOO%22%2C%22AAPL%22%2C%22GOOG%22%2C%22MSFT%22)%0A%09%09&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback="
	f = checkFile()
	if f:
		data = requests.get(url)
		json.dump(data.json(), f)

if __name__ == "__main__":
	init()
