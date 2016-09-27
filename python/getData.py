#!/usr/bin/env python


import requests
import json
import threading
from pytz import timezone
from datetime import datetime
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
import fetch_Ticker_lists
import check
import urllib2

def getDataJSON(stockList, stockTicker):
    listSize = 500
    s_list = stockList
    prefix = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22"
    sufix = "%22)%0A%09%09&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
    eastern_time = datetime.now(timezone('US/Eastern'))
    folder = eastern_time.strftime('%Y_%m_%d')
    check.checkFolder(folder, "../../stData/")
    check.checkFolder(stockTicker, "../../stData/" + folder + "/")
    folder = "../../stData/" + folder + '/' + stockTicker + '/'
    for j in range(0, len(stockList) / listSize + 1):
        query = prefix
        for i in s_list[listSize*j:min(listSize*(j+1),len(stockList))]:
            query += i + '%22%2C%22'
        query = query[0:-9]
        query += sufix
        # url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22YHOO%22%2C%22AAPL%22%2C%22GOOG%22%2C%22MSFT%22)%0A%09%09&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback="
    	filename = eastern_time.strftime('%Y_%m_%d_%H_%M_%S') + '_part' + str(j+1)
        if not(check.checkFile(filename, folder)):
            f = open(folder + filename, 'w')
            data = requests.get(query)
            json.dump(data.json(), f)

def getDataCSV(stockList, stockTicker):
    listSize = 200
    s_list = stockList
    prefix = "http://finance.yahoo.com/d/quotes.csv?s="
    sufix = "&f=sabma5b6vk3lm3m4"
    eastern_time = datetime.now(timezone('US/Eastern'))
    folder = eastern_time.strftime('%Y_%m_%d')
    check.checkFolder(folder, "../../stData/")
    check.checkFolder(stockTicker, "../../stData/" + folder + "/")
    folder = "../../stData/" + folder + '/' + stockTicker + '/'
    for j in range(0, len(stockList) / listSize + 1):
        query = prefix
        for i in s_list[listSize * j:min(listSize * (j + 1), len(stockList))]:
            query += i + '+'
        query = query[0:-1]
        query += sufix
        # url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22YHOO%22%2C%22AAPL%22%2C%22GOOG%22%2C%22MSFT%22)%0A%09%09&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback="
        filename = eastern_time.strftime('%Y_%m_%d_%H_%M_%S') + '_part' + str(j + 1) + '.csv'
        if not (check.checkFile(filename, folder)):
            f = open(folder + filename, 'w')
            response = urllib2.urlopen(query)
            f.write("Symbol,Ask,Bid,Range,AskSize,BidSize,Volume,LastTradeSize,LastTradeWithTime,Average50Days,Average200Days\n")
            f.write(response.read())
            f.close()



# getData(stockList)
def getStockList(stockTicker, eastern_time):
    filename = "../../stData/list/" + eastern_time.strftime('%Y_%m_%d') + '/' + stockTicker  + "stockTicker.txt"
    f = open(filename, 'r')
    content = f.readlines()
    ret = []
    for line in content:
        l = line.split(' ')
        #print l[len(l)-1].strip()[1:-1]
        # #ret.append(l[len(l)-1].strip()[1:-1])
        ret.append(line.strip())
    return ret

def init(interval):
    eastern_time = datetime.now(timezone('US/Eastern'))
    cal = calendar()
    holidays = cal.holidays(start='2014-01-01', end='2020-12-31').to_pydatetime()
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    timenow = eastern_time.hour + float(eastern_time.minute) / 60
    if not(eastern_time.date() in holidays) and (eastern_time.isoweekday() in range(1, 6)) and timenow >= 0 and timenow <= 4 :
        fetch_Ticker_lists.fetch_Ticker_list()
    threading.Timer(interval, init, [interval]).start()
    stockTickerList = ["NASDAQ", "NASDAQTest", "NYSE", "NYSEARCA", "NYSEMKT", "BATS", "OtherTest" ]
    if not(eastern_time.date() in holidays) and (eastern_time.isoweekday() in range(1, 6)) and timenow >= 4 and timenow <= 24:
        for i in range(0,6) :
            stockTicker = stockTickerList[i]
            print "Get data from " + stockTicker + ' @ ' + eastern_time.strftime(fmt)
            stockList = getStockList(stockTicker, eastern_time)
            getDataCSV(stockList, stockTicker)
    else :
        print 'Market is closed now and current time is ' +  eastern_time.strftime(fmt)



if __name__ == "__main__":
    init(60)

