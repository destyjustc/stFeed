import json
import os
import urllib
import csv
from pprint import pprint

file_list = os.listdir('/home/user/Documents/stFeed/files/')

# for file in file_list :
#     if file.find("2016_09_12") != -1 :
#         with open('/home/user/Documents/stFeed/files/' + file) as data_file:
#             data = json.load(data_file)
#         pprint(data)
#         if data.keys[0].find("error") != -1:
#             for i in range(0,1) :
#                 pprint(data["query"]["results"]["quote"][i]['symbol']+':' + data["query"]["results"]["quote"][i]['symbol'])
#                 pprint(data["query"]["results"]["quote"][0])
#                 pprint(file_list[0])


f = urllib.urlopen("http://ichart.finance.yahoo.com/table.csv?s=YHOO&d=8&e=12&f=2016&g=d&a=8&b=1&c=2016&b2&a&ignore=.csv")
values = csv.reader(f)

for row in values:
    print ', '.join(row)