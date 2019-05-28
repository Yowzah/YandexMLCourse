import json
import csv
import pandas as pd
from collections import defaultdict
from atpbar import atpbar
import time

def main():
    list_numbers = getList()
    counter = 0
    data = None
    
    for i in atpbar(range(SIZE), name='GLOBAL'):
        path = getPath(counter, list_numbers)
        dataJson = readJSON(path)
        if (i == 0): 
            indexList = getIndexList(dataJson)
            data = getDataFrame()
        smalldata = writeData(indexList,dataJson, i)
        data = data.append(smalldata, ignore_index=True, sort = False)
        counter = counter + 1
    csv_name = DATASET_NAME +'_' + str(SIZE * SEPARATION) + '_OUT.csv'    
    data.to_csv(csv_name, sep='\t', encoding='utf-8', index=False)
    print('Check ' + str(len(data) == SEPARATION * SIZE))

def getPath(counter, list_numbers):
    filepath = DATASET_NAME + FOLDER_PATH + '/'+ PATTERN + str(list_numbers[counter]) + '.json'
    return filepath

def readJSON(path):
    dataJSON = []
    for line in open(path, 'r'):
        dataJSON.append(json.loads(line))
    return dataJSON

def getIndexList(dataJson): #for first step, make const
    indexSet = set()
    for i in dataJson:
        for k in i.keys():
            if(k != '_source'): indexSet.add(k)
        for j in i['_source'].keys():
            indexSet.add(j)
    indexList = list(indexSet)
    return indexList

def getDataFrame():  
    pattern = defaultdict(list)
    
    return pd.DataFrame.from_dict(pattern)

def writeData(indexList,dataJson,i):
    data = getDataFrame()
    for n in atpbar(range(len(dataJson)), name='LOCAL {}'.format(i)):
        pattern = defaultdict(list)
        for g in indexList: 
            pattern[g].append(None)
        for k in dataJson[n].keys():
            if(k != '_source'): pattern[k] = dataJson[n][k]
        for j in dataJson[n]['_source'].keys(): pattern[j] = dataJson[n]['_source'][j]
        data = data.append(pd.DataFrame.from_dict(pattern), ignore_index=True, sort = False)
    return data

def getList():
    list_numbers = []
    for i in range(10):
        list_numbers.append('0'+str(i))
    for i in range(10,90):
        list_numbers.append(str(i))
    for i in range(9000,9900):
        list_numbers.append(str(i))
    for i in range(990000, LAST_NUMBER + 1):
        list_numbers.append(str(i))
    return list_numbers

FOLDER_PATH = '/parts'
DATASET_NAME = 'logs-tcp-2018.12.11'
LAST_NUMBER = 991013
SEPARATION = 10000
SIZE = 2004
PATTERN = 'ex'

START_TIME = time.time()
print('Process is started: DATASET_NAME - %s, SEPARATION - %d, SIZE - %d' % (DATASET_NAME, SEPARATION, SIZE))
main()
END_TIME = time.time()
print(END_TIME - START_TIME)

#mkdir parts && cd parts && split -d -l 10000 --additional-suffix=.json ../data.json ex && cd ..