# -*- coding: utf-8 -*-

import pymongo 

import json
import datetime,time
import copy
import sys, os


def getTimestampFromDatetime(d=None):
    if d is None:
        d = datetime.datetime.now()
    return time.mktime(d.timetuple())

if __name__ == '__main__':    
    start = getTimestampFromDatetime()
    client = pymongo.MongoClient("127.0.0.1", 27017)
    db = client.csdn2

    file_name = './line.txt'
    fp = open(file_name)
    line = ''
    saveData = []
    
    i = 0
    while True:
        
        i = i+1 
        
        line = fp.readline()
        
        if line == '':
            break
        arr = line.split('#')
        
        target = {}
        
        target['name'] = arr[0].strip()
        target['nickname'] = arr[1].strip()
        target['email'] = arr[2].strip()
        
        #print target
        saveData.append(target) 
        
        if i%100000 == 0 :
            db.user.insert(saveData)
            print i , ' line is insert ' 
            saveData = []
        
        pass

    
    '''
    for i in range(0, 100000):
        saveData.append({
            'count':i
        }) 
    '''

    db.user.insert(saveData)
    print i , ' line is insert ' 
    saveData = []
    
    end = getTimestampFromDatetime()
    print('time: {0}s'.format(end-start))
