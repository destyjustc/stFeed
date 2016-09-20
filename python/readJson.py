import json
import os
import urllib
import csv
from pprint import pprint

folder_list = os.listdir('/home/user/Documents/stFeed/data/')

for folder in folder_list :
    if file.find("2016_09_12") != -1 :
        with open('/home/user/Documents/stFeed/files/' + file) as data_file:
            data = json.load(data_file)
        pprint(data)
        if data.keys[0].find("error") != -1:
            for i in range(0,1) :
                pprint(data["query"]["results"]["quote"][i]['symbol']+':' + data["query"]["results"]["quote"][i]['symbol'])
                pprint(data["query"]["results"]["quote"][0])
                pprint(file_list[0])





