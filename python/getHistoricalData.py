#!/usr/bin/env python

import urllib2
from datetime import datetime, timedelta
from pytz import timezone
import os.path, time
import logging

def totimestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6

def getHistoricalData(market, tickerList):
    eastern_time = datetime.now(timezone('US/Eastern'))
    fmt = "%Y-%m-%d"
    date = eastern_time.strftime(fmt)
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename='logs/getHistoricalData_' + date + '.log', level=logging.WARNING, format=FORMAT)
    prefix = 'http://ichart.finance.yahoo.com/table.csv?s='
    suffix = '&g=d&ignore=.csv'
    for ticker in tickerList:
        url = prefix + ticker + suffix
        try:
            response = urllib2.urlopen(url)
            filename = '../../stData/historicalData/' + market + '/' + ticker + '.csv'
            logging.info(url)
            history_file = open(filename, 'w')
            history_file.write(response.read())
            history_file.close()
        except Exception, e:
            logging.warning(ticker + ' :' + e.message)
            pass

def getTodayData(market, ticker):
    eastern_time = datetime.now(timezone('US/Eastern'))
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



#stockMarketList = ["NASDAQ", "NASDAQTest", "NYSE", "NYSEARCA", "NYSEMKT", "BATS", "OtherTest" ]
#for i in range(0, 6):
#    stockMarket = stockMarketList[i]
#    eastern_time = datetime.now(timezone('US/Pacific'))
#    fmt = "%Y-%m-%d"
#    print "Get data from " + stockMarket + ' @ ' + eastern_time.strftime(fmt)
#    stockList = getStockList(stockMarket, eastern_time)
#    getHistoricalData(stockMarket, stockList)