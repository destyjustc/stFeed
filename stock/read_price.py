import string
import urllib2
from bs4 import BeautifulSoup


global f

url_part1 = 'http://ichart.finance.yahoo.com/table.csv?s='
url_part2 = '&d=8&e=12&f=2016&g=d&a=8&b=1&c=2016&sn=a&ignore=.csv'

print "Starting"

f = open('stock_names.txt', 'r')
file_content = f.readlines()
count = 1;
print "About %d tickers will be downloaded" % len(file_content)

for ticker in file_content:
    ticker = ticker.strip()
    url = url_part1 + ticker + url_part2

    try:
        # This will cause exception on a 404
        response = urllib2.urlopen(url)
        print "Downloading ticker %s (%d out of %d)" % (ticker, count, len(file_content))
        count = count + 1
        history_file = open('/home/user/Documents/Historical_Data/' + ticker + '.csv', 'w')
        history_file.write(response.read())
        history_file.close()
    except Exception, e:
        print e.code
        print e.msg
        pass

f.close()