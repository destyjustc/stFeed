from flask import Flask
from flaskext.mysql import MySQL
import requests
from pprint import pprint
import json
from os import listdir, walk
import time
import threading
from datetime import datetime, timedelta

def checkFile():
	prefix = time.strftime('%Y_%m_%d_%H_%M_%S')
	exit = False
	for filename in listdir('./files'):
		if filename == prefix:
			exit = True
			break;
	if exit == False:
		f = open('./files/'+prefix, 'w')
		return f

def getData(stockList):
	s_list = stockList
	prefix = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22"
	sufix = "%22)%0A%09%09&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
	for i in s_list:
		prefix += i + '%22%2C%22'
	prefix = prefix[0:-9];
	prefix += sufix
	# url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22YHOO%22%2C%22AAPL%22%2C%22GOOG%22%2C%22MSFT%22)%0A%09%09&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback="
	f = checkFile()
	if f:
		data = requests.get(prefix)
		json.dump(data.json(), f)

def getStockList(filename):
	f = open(filename, 'r')
	content = f.readlines()
	ret = []
	for line in content:
		l = line.split(' ')
		# print l[len(l)-1].strip()[1:-1]
		ret.append(l[len(l)-1].strip()[1:-1])
	return ret

def init(interval, stockList):
	print "Get data"
	threading.Timer(interval, init, [interval, stockList]).start()	 
        from pytz import timezone
	eastern = timezone('US/Eastern')
	fmt = '%Y-%m-%d %H:%M:%S %Z%z'	
	loc_dt = eastern.localize(time.gmtime())
	print loc_dt.strftime(fmt)
	
	
	getData(stockList)

if __name__ == "__main__":
	stockList = getStockList("./files/stock_list")
	init(10, stockList)
