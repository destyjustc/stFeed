import json
import os, glob
import urllib
import csv
from pprint import pprint

prefix = '../data/'
folder_list = os.listdir(prefix)

for folder in folder_list :
    if os.path.isdir(prefix+folder) :
        print folder
        timepoint_list = os.listdir('../data/' + folder + '/')
        for timepoint in timepoint_list :
            if not timepoint.startswith('.') and timepoint.endswith('1') :
                file_list = glob.glob(prefix + folder + '/' + timepoint[:-1] +'*')
                #print prefix + folder + '/' + file[:-1] +'*'
                for file in file_list:
                    with open(file) as data_file:
                        data = json.load(data_file)
                        #pprint(data["query"]["results"]["quote"][0])
                        if data["query"]["results"]["quote"][0]["symbol"] == 'GOOG' :
                            pprint(data["query"]["results"]["quote"][0])

        #    for i in range(0,1) :
         #       pprint(data["query"]["results"]["quote"][i]['symbol']+':' + data["query"]["results"]["quote"][i]['symbol'])
         #       pprint(data["query"]["results"]["quote"][0])
          #      pprint(file_list[0])





