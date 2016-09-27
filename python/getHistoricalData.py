#!/usr/bin/env python

import urllib2
from datetime import datetime
from pytz import timezone
from getData import getStockList

def getHistoricalData(market, tickerList):
    prefix = 'http://ichart.finance.yahoo.com/table.csv?s='
    suffix = '&g=d&ignore=.csv'
    for ticker in tickerList:
        url = prefix + ticker + suffix
        print url
        try:
            response = urllib2.urlopen(url)
            history_file = open('../../stData/historicalData/' + market + '/' + ticker + '.csv', 'w')
            history_file.write(response.read())
            history_file.close()
        except Exception, e:
            print str(e.code) + ":" + e.msg
            pass

def getTodayData(market, ticker):
    eastern_time = datetime.now(timezone('US/Pacific'))
    fmt = "%Y-%m-%d"
    date = eastern_time.strftime(fmt)
    print date
    Year = date[0:4]
    Month = str(int(date[5:7])-1)
    Day = date[8:10]
    prefix = 'http://ichart.finance.yahoo.com/table.csv?s='
    suffix = '&b=' + Day + '&a=' + Month + '&c=' + Year +'&g=d&ignore=.csv'
    url = prefix + ticker + suffix
    todayData = urllib2.urlopen(url)
    row = todayData.readlines()
    print row[1]
    history_file = open('../../stData/historicalData/' + market + '/' + ticker + '.csv', 'r')
    historyData = history_file.readlines()
    history_file.close()
    historyData.insert(1,row[1])
    history_file = open('../../stData/historicalData/' + ticker + '.csv', 'w')
    historyData="".join(historyData)
    history_file.write(historyData)
    history_file.close()

stockMarketList = ["NASDAQ", "NASDAQTest", "NYSE", "NYSEARCA", "NYSEMKT", "BATS", "OtherTest" ]

for i in range(0, 6):
    stockMarket = stockMarketList[i]
    eastern_time = datetime.now(timezone('US/Pacific'))
    fmt = "%Y-%m-%d"
    print "Get data from " + stockMarket + ' @ ' + eastern_time.strftime(fmt)
    stockList = getStockList(stockMarket, eastern_time)
    getHistoricalData(stockMarket, stockList)