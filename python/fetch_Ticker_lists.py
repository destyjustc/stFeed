from datetime import datetime
from pytz import timezone
import os
import ftplib
import requests
import check
import logging

eastern_time = datetime.now(timezone('US/Eastern'))
fmt = "%Y-%m-%d"
date = eastern_time.strftime(fmt)
logging.basicConfig(filename='logs/fetch_Ticker_lists_' + date + '.log', level=logging.WARNING)

def fetch_file(remoteFile, localFile, folder):
    prefix = '../../stData/list/'
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
        ticker = ticker.replace(".", '-')
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
        except ValueError as e:
            logging.warning(ticker+':'+ e.message)
            pass
        except requests.exceptions.RequestException  as e:
            logging.warning(ticker+ ':' + e.message)
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
        ticker = split[7][:-2]
        ticker =  ticker.replace(".", '-')
        Exchange = split[2]
        test = split[6]
        query = prefix + ticker + sufix
        # print query
        try:
            data = requests.get(query)
            if data.status_code == 400 :
                print "No json for " + ticker
                foutNULL.write(ticker + ' error code: 400 \n')
            else :
                data = data.json()
                 #  response = urllib2.urlopen(url)
                if data["query"]["results"] is None  :
                    print "result is null for " + ticker
                    foutNULL.write(ticker + ' is null \n')
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
        except ValueError as e:
            print e
            pass
        except requests.exceptions.RequestException as e:
            print e
            pass



def fetch_Ticker_list():
    eastern_time = datetime.now(timezone('US/Eastern'))
    fmt = '%Y_%m_%d'
    prefix = '../../stData/list/' + eastern_time.strftime(fmt) + '/'
    localFile1 = "NASDAQ.txt"
    localFile2 = "NASDAQ_Other.txt"
    remoteFile1 = "nasdaqlisted.txt"
    remoteFile2 = "otherlisted.txt"
    fetch_file(remoteFile1, localFile1, eastern_time.strftime(fmt))
    fetch_file(remoteFile2, localFile2, eastern_time.strftime(fmt))
    num_lines_NASDAQ = sum(1 for line in open(prefix + localFile1))
    num_lines_Other = sum(1 for line in open(prefix + localFile2))
    stockTicker = ["NASDAQstockTicker.txt", "NASDAQTeststockTicker.txt", "NASDAQNULLstockTicker.txt"]
    num_lines_NASDAQstock = 2
    for i in range(0,3):
        if os.path.isfile(prefix + stockTicker[i]):
            num_lines_NASDAQstock += sum(1 for line in open(prefix + stockTicker[i]))


    if num_lines_NASDAQ != num_lines_NASDAQstock :
        fout1 = open(prefix + stockTicker[0], 'w')
        fout2 = open(prefix + stockTicker[1], 'w')
        foutNULL = open(prefix + stockTicker[2], 'w')
        getNASDAQTicker(fout1, fout2, foutNULL, prefix  + localFile1)
        fout1.close()
        fout2.close()
        foutNULL.close()

    stockTicker = ["NYSEMKTstockTicker.txt", "NYSEstockTicker.txt", "NYSEARCAstockTicker.txt", "BATSstockTicker.txt", "OtherTeststockTicker.txt","NULLOtherstockTicker.txt"]

    num_lines_OtherStock = 2

    for i in range(0,6):
        if os.path.isfile(prefix + stockTicker[i]):
            num_lines_OtherStock += sum(1 for line in open(prefix + stockTicker[i]))



    if num_lines_Other != num_lines_OtherStock :
        fout1 = open(prefix  + stockTicker[0], 'w')
        fout2 = open(prefix  + stockTicker[1], 'w')
        fout3 = open(prefix  + stockTicker[2], 'w')
        fout4 = open(prefix  + stockTicker[3], 'w')
        fout5 = open(prefix  + stockTicker[4], 'w')
        foutNULL = open(prefix  + stockTicker[5], 'w')
        getOtherTicker(fout1, fout2, fout3, fout4, fout5, foutNULL, prefix  + localFile2)
        fout1.close()
        fout2.close()
        fout3.close()
        fout4.close()
        fout5.close()
        foutNULL.close()


   # getTicker(fout, prefix + localFile2)



