#!/usr/bin/env python

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
import os
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

def checkfolder(folder):
	exit = False
	for foldername in listdir('../data'):
		if foldername == folder:
			exit = True;
			break;
	if exit == False :
		os.makedirs('../data/' +folder)

def checkFile(prefix):
	
	exit = False
	for filename in listdir('../data'):
		if filename == prefix:
			exit = True
			break;
	if exit == False:
		f = open('../data/'+prefix, 'w')
		return f

def getData(stockList):
	listSize = 1200
	s_list = stockList
	prefix = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22"
	sufix = "%22)%0A%09%09&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
	pacific_time = datetime.now(timezone('US/Pacific'))
	for j in range(0, len(stockList) / listSize + 1):
		print j
		query = prefix
		for i in s_list[listSize*j:min(listSize*(j+1),len(stockList))]:
			query += i + '%22%2C%22'
		query = query[0:-9];
		query += sufix
			# url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22YHOO%22%2C%22AAPL%22%2C%22GOOG%22%2C%22MSFT%22)%0A%09%09&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback="
		

		folder = pacific_time.strftime('%Y_%m_%d')
		checkfolder(folder)
		filename = folder + '/' + pacific_time.strftime('%Y_%m_%d_%H_%M_%S')
		f = checkFile(filename)

		print f
		if f:
			#print query
			data = requests.get(query)
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
	threading.Timer(interval, init, [interval, stockList]).start()
	cal = calendar()
	holidays = cal.holidays(start='2014-01-01', end='2020-12-31').to_pydatetime()
	fmt = "%Y-%m-%d %H:%M:%S %Z%z"
	pacific_time = datetime.now(timezone('US/Pacific'))
	eastern_time = datetime.now(timezone('US/Eastern'))
	timenow = eastern_time.hour + float(eastern_time.minute) / 60
	if not(datetime.now().date() in holidays) and (datetime.now().isoweekday() in range(1, 6)) and timenow >= 9 and timenow <= 17:
		print "Get data"
		print time.strftime("%Y-%m-%d %H:%M:%S %Z%z", time.gmtime())
		fmt = "%Y-%m-%d %H:%M:%S %Z%z"
		pacific_time = datetime.now(timezone('US/Pacific'))
		print pacific_time.strftime(fmt)
		eastern_time = datetime.now(timezone('US/Eastern'))
		print eastern_time.strftime(fmt)
		getData(stockList)
	else:
		print 'Market is closed now and current time is ' +  eastern_time.strftime(fmt)

	#getData(stockList)

if __name__ == "__main__":
	stockList = getStockList("../files/stock_names.txt")
	init(60, stockList)
