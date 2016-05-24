# -*- coding: utf-8 -*-

import sys
from pip._vendor.requests.models import json_dumps
from pyasn1.compat.octets import null
reload(sys)
sys.setdefaultencoding('utf-8')

'''

建立POI信息表

'''
import mysql.connector
from bs4 import BeautifulSoup
from bs4.element import Tag 
import os
import time
import json
import re

def safeStr(s):
    return s.replace("'", "")

def log( msg):
    print msg
    _path = './logs/buildpoi/' ;
    if not os.path.isdir(_path) :
        try:
            os.makedirs(_path)
        except OSError:
            print 'create ' + _path + ' failed '
            return
        pass
        
    _file = _path + time.strftime('%m%d') + '.log'
    
    fp = open(_file, 'a')
    
    fp.write(time.strftime('%Y-%m-%d %H:%M:%S :') + msg + "\n")
    fp.close()

def parseInt(str_num):
    num = 0 
    try:
        num = int(str_num)
    except ValueError as ve:
        #print str(ve)
        pass
    return num

def myParse(html):
    
    rdict = {
             'detail' : '' ,
             'kvs' : '' ,
             'lon' : '' ,
             'lat' : '' ,
             'qy_pid' : 0
             }

    bsobj = BeautifulSoup(html, 'lxml')
    
    # 详情
    rdict['detail'] = ''
    node = bsobj.findAll("div", {"class":"poiDet-detail"})
    if len(node) > 0 :
        rdict['detail'] = node[0].get_text().strip()
        pass
    
    # KV
    kv_nodes = bsobj.find("ul", {"class":"poiDet-tips"}).children

    kv_list = []
    for _kv_li in kv_nodes :
        if isinstance(_kv_li, Tag) :
            
            #print type(_kv_li)
            try :
                _k = _kv_li.find("span", {"class":"title"}).get_text().strip()
                _v = _kv_li.find("div", {"class":"content"}).p.get_text().strip().replace(u'(查看地图)','')
                #print _k, ' = ', _v 
                _k = safeStr(_k)
                _v = safeStr(_v)
                kv_list.append({'k':_k, 'v':_v})
            except AttributeError as e :
                log(str(e))
            
            pass
        pass
        
    #print kv_list
    rdict['kvs'] = json.dumps(kv_list)
    
    # 经纬度
    #location_img_tag = bsobj.find("img", {"src": re.compile("")})
    location_re = re.compile("http\:\/\/maps\.google\.cn.*\|(.*?)\,(.*?)\&sensor\=false")
    searchobj = location_re.search(html)
    if searchobj :
        location_pair = searchobj.groups()
        print location_pair
        if len(location_pair) >= 2 :
            rdict['lat'] = location_pair[0]
            rdict['lon'] = location_pair[1]
    else:
        print 'no match'
        
    #pid
    #pid_re = re.compile("\{.*?TYPE.*?\:.*?\'poi\'.*?\,.*?PID.*?\:.*?\'(\d+)\'.*?\}", re.IGNORECASE|re.MULTILINE)
    pid_re = re.compile("PID.*?\:.*?\'(\d+)\'", re.IGNORECASE|re.MULTILINE)
    searchobj = pid_re.search(html)
    if searchobj :
        pid_val = searchobj.groups()
        rdict['qy_pid'] = parseInt(pid_val[0])
    else:
        #print 'not'
        pass
    return rdict

#sys.argv
print sys.argv

if len(sys.argv) < 2 :
    print 'usage : python buildpoi.py Asialist '
    #'Asialist', 'Europelist', 'Africalist', 'NorthAmericalist', 'SouthAmericalist', 'Oceanialist', 'Antarcticalist'
    exit()
    pass

continent = sys.argv[1]
print 'now exec ' , continent , ' datas ... '

cnx = None

def connect_mysql():
    global cnx
    config = {
          'user':'root',
          'password':'lixinxin',
          'host':'SpiderDb',
          'database':'qy_spider'
          }
    log('connection to ' + config['host'])
    cnx = mysql.connector.connect(**config)
    cnx.cursor().execute("set names utf8")

connect_mysql()

xcur = cnx.cursor()
xcur.execute("select id,name,filepath from travels where status=1 and poi_status=0 and continent='"+continent+"' order by id asc limit 10") 
result = xcur.fetchall()
#print result
print 'total : ' , len(result) , 'row '
for (id,name,filepath) in result:
    
    _path = '../startdemo/'+filepath
    
    if not os.path.exists(_path):
        log(_path + ' is not exist')
    
    if not os.path.isfile(_path):
        log(_path + ' is not a file')
        
    
    fp = open(_path)
    html = fp.read()
    result_dict = myParse(html)
    print result_dict
    fp.close()
    pass


'''
fp = open('../startdemo/travel_htmls/demo.html')
html = fp.read()
#print html
result_dict = myParse(html)
print result_dict
fp.close()

'''