from datetime import datetime
from pytz import timezone
from os import listdir
import urllib2
import ftplib

global prefix
global count

prefix = '../data/list/'
count = 0

def fetch_file(remoteFile, localFile):
    ftp = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp.login()
    ftp.cwd("symboldirectory")
    exit = False
    for filename in listdir(prefix):
        if filename == localFile:
            exit = True
            break;
    if exit == False:
        f = open(prefix + localFile, 'w')
        ftp.retrbinary("RETR " + remoteFile, f.write)
    ftp.quit()

def getTicker(fout, filename):

    url_part1 = 'http://ichart.finance.yahoo.com/table.csv?s='
    url_part2 = '&d=8&e=12&f=2016&g=d&a=8&b=1&c=2016&sn=a&ignore=.csv'
    with(open(filename, 'r')) as fin:
        lines = fin.readlines()
    fin.close()
    for line in lines[1:-1]:
        ticker =  line.split('|')[0]
        url = url_part1 + ticker + url_part2
        print url
        try:
            response = urllib2.urlopen(url)
            count = count + 1
            print "ticker %d : %s " % (count, ticker)
            fout.write(ticker + '\n')
        except Exception, e:
            print e.code
            print e.msg
            pass



def fetch_Ticker_list():

    eastern_time = datetime.now(timezone('US/Eastern'))
    localFile1 = "NASDAQ_" + eastern_time.strftime('%Y_%m_%d')
    localFile2 = "NASDAQ_Other_" + eastern_time.strftime('%Y_%m_%d')
    remoteFile1 = "nasdaqlisted.txt"
    remoteFile2 = "otherlisted.txt"

    fetch_file(remoteFile1, localFile1)
    fetch_file(remoteFile2, localFile2)

    stockTicker = "stockTicker_" + eastern_time.strftime('%Y_%m_%d') + ".txt"

    exit = False
    for filename in listdir(prefix):
        if filename == stockTicker:
            exit = True
            break
    if exit == False:
        fout = open(prefix + stockTicker, 'w')
        getTicker(fout, prefix + localFile1)
        getTicker(fout, prefix + localFile2)
        fout.close()

fetch_Ticker_list()
