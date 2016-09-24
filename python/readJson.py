import json
import os, glob
import urllib
import csv
from pprint import pprint
import matplotlib.pyplot as plt
prefix = '../data/'
mtime = lambda f: os.stat(os.path.join(prefix, f)).st_mtime

folder_list =  list(sorted(os.listdir(prefix), key=mtime))
ask_list = list()
bid_list = list()
time_list = list()
for folder in folder_list :
    if os.path.isdir(prefix+folder) :
        path = '../data/' + folder + '/NASDAQ/' + folder
        timepoint_list = sorted(glob.glob(path + "*1" ))
        for timepoint in timepoint_list:
            file_list = glob.glob(timepoint[:-1] +'*')
                #print prefix + folder + '/' + file[:-1] +'*'
            for file in file_list:
                with open(file) as data_file:
                    data = json.load(data_file)["query"]["results"]["quote"]
                    for i in range(0, len(data)):
                        if data[i]["symbol"] == "AAPL" :
                          #  pprint(data[i])
                            pprint('Ask: ' + data[i]['Ask'] + ' Bid: ' + data[i]['Bid'] + ' @ ' + file[26:45])
                            #pprint(data[i]['LastTradeWithTime'])
                            ask_list.append(data[i]['Ask'])
                            bid_list.append(data[i]['Bid'])
                            time_list.append(file[26:45])



        #    for i in range(0,1) :
         #       pprint(data["query"]["results"]["quote"][i]['symbol']+':' + data["query"]["results"]["quote"][i]['symbol'])
         #       pprint(data["query"]["results"]["quote"][0])
          #      pprint(file_list[0])





