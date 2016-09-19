from flask import Flask
from flaskext.mysql import MySQL
import requests
from pprint import pprint
import json
from os import listdir, walk
import time
import threading
from pytz import timezone
from datetime import datetime, timedelta
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

def checkFile():
	pacific_time = datetime.now(timezone('US/Pacific'))
	prefix = pacific_time.strftime('%Y_%m_%d_%H_%M_%S')
	exit = False
	for filename in listdir('../data'):
		if filename == prefix:
			exit = True
			break;
	if exit == False:
		f = open('../data/'+prefix, 'w')
		return f

def getData(stockList):
	s_list = stockList
	#print stockList
	prefix = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22"
	sufix = "%22)%0A%09%09&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
	for i in s_list:
		prefix += i + '%22%2C%22'
	prefix = prefix[0:-9];
	prefix += sufix
	# url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22YHOO%22%2C%22AAPL%22%2C%22GOOG%22%2C%22MSFT%22)%0A%09%09&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback="
	f = checkFile()
	if f:
		print prefix
		data = requests.get(prefix)
		json.dump(data.json(), f)

def getStockList(filename):
	f = open(filename, 'r')
	content = f.readlines()
	ret = []
	for line in content:
		l = line.split(' ')
		#print l[len(l)-1].strip()[1:-1]
		#ret.append(l[len(l)-1].strip()[1:-1])
		ret.append(line.strip())
	return ret

def init(interval, stockList):
	print "Get data"
	threading.Timer(interval, init, [interval, stockList]).start()

	cal = calendar()
	holidays = cal.holidays(start='2014-01-01', end='2020-12-31').to_pydatetime()
	fmt = "%Y-%m-%d %H:%M:%S %Z%z"
	pacific_time = datetime.now(timezone('US/Pacific'))
	eastern_time = datetime.now(timezone('US/Eastern'))
	timenow = eastern_time.hour + float(eastern_time.minute) / 60
	if not(datetime.now().date() in holidays) and (datetime.now().isoweekday() in range(6, 8)) and timenow >= 9 and timenow <= 19:
		print time.strftime("%Y-%m-%d %H:%M:%S %Z%z", time.gmtime())
		fmt = "%Y-%m-%d %H:%M:%S %Z%z"
		pacific_time = datetime.now(timezone('US/Pacific'))
		print pacific_time.strftime(fmt)
		eastern_time = datetime.now(timezone('US/Eastern'))
		print eastern_time.strftime(fmt)
		getData(stockList)
	else:
		print 'Market is closed now'

	#getData(stockList)

if __name__ == "__main__":
	stockList = getStockList("../files/stock_names.txt")
	init(60, stockList)
