#!/usr/bin/env python

import requests
from pytz import timezone
from datetime import datetime
import threading
import sys
import csv
import argparse
import urllib2


def getRealTimeDataJSON(tickers, interval):
    eastern_time = datetime.now(timezone('US/Eastern'))
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    prefix = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22"
    sufix = "%22)%0A%09%09&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
    if ',' in tickers :
        ticker_list = tickers.split(',')
    else:
        ticker_list = [tickers]
    query = prefix
    for ticker in ticker_list:
        query  += ticker + '%22%2C%22'
    query = query[0:-9]
    query += sufix
    data = requests.get(query)
    print "Get data at " + eastern_time.strftime(fmt)
    if data.status_code == 400:
        print "No json for " + ticker
    else:
        data = data.json()
        #  response = urllib2.urlopen(url)
        if data["query"]["results"] is None:
            print "result is null for " + ticker
        else :
            data = data["query"]["results"]["quote"]
            if not isinstance(data, list):
                data = [data]
            for i in range(0, len(data)):
                if data[i]["Ask"] is None:
                    print data[i]["Symbol"] + ": no data"
                else:
                    #print data[i]
                    print data[i]["Symbol"] + " Ask : " + data[i]["Ask"] + " Bid : " + data[i]["Bid"]
    threading.Timer(interval, getRealTimeDataJSON, [tickers, interval]).start()

def getRealTimeDataCSV(tickers, interval):
    eastern_time = datetime.now(timezone('US/Eastern'))
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    prefix = "http://finance.yahoo.com/d/quotes.csv?s="
    sufix = "&f=sabd1t1b1b2k1n"
    if ',' in tickers :
        ticker_list = tickers.split(',')
    else:
        ticker_list = [tickers]
    query = prefix
    for ticker in ticker_list:
        query  += ticker + '+'
    query = query[0:-1]
    query += sufix
    data = urllib2.urlopen(query)
    cr = csv.reader(data)
    count = 0
    print "Get data at " + eastern_time.strftime(fmt)
    for row in cr:
        if row[0] == "N/A":
            print "No data for " + ticker_list[count]
        else:
            print  row[0] + " Ask:" + row[1] + " Bid:" + row[2] + ' Last trade time and date: ' + row[3] + " " + row[4] + " Realtime  Ask : " + row[5] + " Realtime Bid : " + row[6] +  ' Last trade realtime: ' + row[7] + " " +row[8]
        count = count + 1;
    threading.Timer(interval, getRealTimeDataCSV, [tickers, interval]).start()


def main(args):
    input = args.t
    interval = args.i
    if args.f == "CSV" :
        getRealTimeDataCSV(input, interval)
    else:
        getRealTimeDataJSON(input, interval)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=str, default="AAPL,GOOG")
    parser.add_argument('-i', type=int, default= 60)
    parser.add_argument('-f', type=str, default= "CSV")
    args = parser.parse_args()

    sys.exit(main(args=args))
