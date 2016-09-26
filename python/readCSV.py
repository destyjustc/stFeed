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
        timepoint_list = sorted(glob.glob(path + "*part1.csv" ))
        for timepoint in timepoint_list:
            file_list = glob.glob(timepoint[:-5] +'*')
                #print prefix + folder + '/' + file[:-1] +'*'
            for file in file_list:
                with open(file,'rb') as data_file:
                    data = csv.DictReader(data_file)
                    for line in data:
                      #  print line["Symbol"]
                        if line["Symbol"] == "AAPL" :
                            ask_list.append(data['Ask'])
                            bid_list.append(data['Bid'])


