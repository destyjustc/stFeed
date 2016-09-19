import string
import urllib2
from bs4 import BeautifulSoup

global f

def download_page(url):
    aurl = urllib2.urlopen(url)
    soup = BeautifulSoup(aurl.read())

    print url

    for row in soup('table')[1]('tr'):
        tds = row('td')
        if (len(tds) > 0):
            f.write(tds[1].string + '\n')


f = open('../files/stock_names.txt', 'w')

url_part1 = 'http://en.wikipedia.org/wiki/Companies_listed_on_the_New_York_Stock_Exchange_'
url = url_part1 + '(0-9)'
download_page(url)

for letter in string.uppercase[:26]:
    url_part2 = letter
    url = url_part1 + '(' + letter + ')'

    download_page(url)
f.close()