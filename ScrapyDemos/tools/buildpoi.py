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
        #print location_pair
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

def flush_data(_datalist, _idlist):
    global cnx
    
    print 'flush data is exec '
    
    isconn = cnx.is_connected()
    if not isconn :
        log('connection is lose')
        connect_mysql()
        
    #xcur = cnx.cursor()
    #xcur.execute("insert into poi(`travel_id`,`detail`,`kvs`,`addtime`,`lon`,`lat`,`qy_pid`) values()")
        
    
    xcursor = cnx.cursor()
    if len(_datalist) > 0 :
        _values = ",".join(_datalist)
        xcursor.execute("insert into poi(`travel_id`,`detail`,`kvs`,`addtime`,`lon`,`lat`,`qy_pid`) values"+_values)
        cnx.commit()
        pass
        
    if len(_idlist) > 0 :
        _values = ",".join(_idlist)
        xcursor.execute("update travels set poi_status=1 where id in("+_values+")")
        cnx.commit()
        pass
        
    xcursor.close()
        
    return

connect_mysql()

xcur = cnx.cursor()
xcur.execute("select id,name,filepath from travels where status=1 and poi_status=0 and continent='"+continent+"' order by id asc limit 10") 
result = xcur.fetchall()
#print result
print 'total : ' , len(result) , 'row '
datalist = []
idlist = []
for_index = 0
for (id,name,filepath) in result:

    print 'exec ' , id , ' ' , name , ' ... '
    
    _path = '../startdemo/'+filepath
    
    if not os.path.exists(_path):
        log(_path + ' is not exist')
    
    if not os.path.isfile(_path):
        log(_path + ' is not a file')
        
    
    fp = open(_path)
    html = fp.read()
    fp.close()
    
    result_dict = myParse(html)
    
    #print result_dict
    #xcur.execute("insert into poi(`travel_id`,`detail`,`kvs`,`addtime`,`lon`,`lat`,`qy_pid`) values()")
    
    _travel_id = ('%d' %id)
    _detail = result_dict['detail'].replace("'", "")
    _kvs = result_dict['kvs'].replace("'", "")
    _lon = result_dict['lon'].replace("'", "")
    _lat = result_dict['lat'].replace("'", "")
    _qy_pid = ('%d' %result_dict['qy_pid'])
    
    now = int(time.time())
    _addtime = ('%d' %now)
    
    datalist.append("("+_travel_id+", '"+_detail+"', '"+_kvs+"', "+_addtime+", '"+_lon+"', '"+_lat+"', "+_qy_pid+")")
    idlist.append(_travel_id)
    
    for_index = for_index+1
    
    if for_index % 100 == 0 :
        flush_data(datalist, idlist)
        datalist = []
        idlist = []
    
    print 'exec ' , id , ' ' , name , ' done! '
    
    pass

flush_data(datalist, idlist)
datalist = []
idlist = []