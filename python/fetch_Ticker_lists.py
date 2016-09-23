from datetime import datetime
from pytz import timezone
import os
import ftplib
import requests
import check

def fetch_file(remoteFile, localFile, folder):
    prefix = '../data/list/'
    check.checkFolder(folder, prefix)
    ftp = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp.login()
    ftp.cwd("symboldirectory")
    exit = False
    if not(check.checkFile(localFile, prefix + folder)) :
        f = open(prefix + folder + '/' + localFile, 'w')
        ftp.retrbinary("RETR " + remoteFile, f.write)
        f.close()
    ftp.quit()

def getNASDAQTicker(fout1, fout2, foutNULL, filename):
    countNASDAQ = 0
    countNASDAQtest = 0
    prefix = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22"
    sufix = "%22)%0A%09%09&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
    with(open(filename, 'r')) as fin:
        lines = fin.readlines()
    fin.close()
    for line in lines[1:-1]:
        split =  line.split('|')
        ticker = split[0]
        test = split[3]
        query = prefix + ticker + sufix
        try:
            data = requests.get(query).json()
            if data["query"]["results"] is None  :
                print "result is null for " + ticker
                foutNULL.write(ticker + '\n')
            else:
                if test == 'Y' :
                    countNASDAQtest = countNASDAQtest + 1
                    print "NASDAQ test ticker %d : %s " % (countNASDAQtest, ticker)
                    fout2.write(ticker + '\n')
                else:
                    countNASDAQ = countNASDAQ + 1
                    print "NASDAQ ticker %d : %s " % (countNASDAQ, ticker)
                    fout1.write(ticker + '\n')
        except requests.exceptions.RequestException as e:
            print e
            pass


def getOtherTicker(fout1, fout2, fout3, fout4, fout5, foutNULL, filename):
    countNYSEMKT = 0
    countNYSE = 0
    countNYSEARCA = 0
    countBATS = 0
    countTest = 0
    prefix = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22"
    sufix = "%22)%0A%09%09&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
    with(open(filename, 'r')) as fin:
        lines = fin.readlines()
    fin.close()
    for line in lines[1:-1]:
        split =  line.split('|')
        ticker = split[7]
        Exchange = split[2]
        test = split[6]
        query = prefix + ticker + sufix
        # print query
        try:
            data = requests.get(query)
            if data.status_code == 400 :
                print "No json for " + ticker
                foutNULL.write(ticker + ' 400 \n')
            else :
                data = data.json()
                 #  response = urllib2.urlopen(url)
                if data["query"]["results"] is None  :
                    print "result is null for " + ticker
                    foutNULL.write(ticker + '\n')
                else:
                    if test == 'Y' :
                        countTest = countTest + 1
                        print "Other test ticker %d : %s " % (countTest, ticker)
                        fout5.write(ticker + '\n')
                    else:
                        if Exchange == 'A':
                            countNYSEMKT = countNYSEMKT + 1
                            print "NYSEMKT ticker %d : %s " % (countNYSEMKT, ticker)
                            fout1.write(ticker + '\n')
                        if Exchange == 'N':
                            countNYSE = countNYSE + 1
                            print "NYSE ticker %d : %s " % (countNYSE, ticker)
                            fout2.write(ticker + '\n')
                        if Exchange == 'P':
                            countNYSEARCA = countNYSEARCA + 1
                            print "NYSEMKTARCA ticker %d : %s " % (countNYSEARCA, ticker)
                            fout3.write(ticker + '\n')
                        if Exchange == 'Z':
                            countBATS = countBATS + 1
                            print "BATS ticker %d : %s " % (countBATS, ticker)
                            fout4.write(ticker + '\n')
        except requests.exceptions.RequestException as e:
            print e
            pass



def fetch_Ticker_list():
    eastern_time = datetime.now(timezone('US/Eastern'))
    fmt = '%Y_%m_%d'
    prefix = '../data/list/' + eastern_time.strftime(fmt) + '/'
    localFile1 = "NASDAQ.txt"
    localFile2 = "NASDAQ_Other.txt"
    remoteFile1 = "nasdaqlisted.txt"
    remoteFile2 = "otherlisted.txt"

    fetch_file(remoteFile1, localFile1, eastern_time.strftime(fmt))
    fetch_file(remoteFile2, localFile2, eastern_time.strftime(fmt))

    stockTicker1 = "NASDAQstockTicker.txt"
    stockTicker2 = "NASDAQTeststockTicker.txt"
    stockTickerNULL =  "NULLstockTicker.txt"
    exit1 = check.checkFile(stockTicker1, prefix )
    exit2 = check.checkFile(stockTicker2, prefix )


    if exit1 == False or exit2 == False or os.stat(prefix + stockTicker1).st_size == 0 or os.stat(prefix + stockTicker2).st_size == 0:
        fout1 = open(prefix + stockTicker1, 'w')
        fout2 = open(prefix + stockTicker2, 'w')
        foutNULL = open(prefix + stockTickerNULL, 'a')
        getNASDAQTicker(fout1, fout2, foutNULL, prefix  + localFile1)
        fout1.close()
        fout2.close()
        foutNULL.close()


    stockTicker1 = "NYSEMKTstockTicker.txt"
    stockTicker2 = "NYSEstockTicker.txt"
    stockTicker3 = "NYSEARCAstockTicker.txt"
    stockTicker4 = "BATSstockTicker.txt"
    stockTicker5 = "OtherTeststockTicker.txt"

    count = 0

    for filename in os.listdir(prefix ):
        if filename == stockTicker1 or filename == stockTicker2 or filename == stockTicker3 or filename == stockTicker4 or filename == stockTicker5:
            count = count + 1
        if count == 5:
            break

    if count < 5 or os.stat(prefix + stockTicker1).st_size == 0 or os.stat(prefix + stockTicker2).st_size == 0 or os.stat(prefix + stockTicker3).st_size == 0 or os.stat(prefix + stockTicker4).st_size == 0 or os.stat(prefix + stockTicker5).st_size == 0:
        fout1 = open(prefix  + stockTicker1, 'w')
        fout2 = open(prefix  + stockTicker2, 'w')
        fout3 = open(prefix  + stockTicker3, 'w')
        fout4 = open(prefix  + stockTicker4, 'w')
        fout5 = open(prefix  + stockTicker5, 'w')
        foutNULL = open(prefix  + stockTickerNULL, 'a')
        getOtherTicker(fout1, fout2, fout3, fout4, fout5, foutNULL, prefix  + localFile2)
        fout1.close()
        fout2.close()
        fout3.close()
        fout4.close()
        fout5.close()
        foutNULL.close()


   # getTicker(fout, prefix + localFile2)



