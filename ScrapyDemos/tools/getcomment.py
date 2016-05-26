# -*- coding: utf-8 -*-
import urllib2
from urllib import urlencode
from random import random
import mysql.connector
import os
import time
import hashlib
import sys
import json
from cgi import log
import socket

class getcomment(object):
        
    
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    
    
    # http://www.xicidaili.com/    免费http代理服务器
    PROXIES = [
        {'ip_port': '122.96.59.104:80', 'user_pass': ''},
        {'ip_port': '119.188.94.145:80', 'user_pass': ''},
        {'ip_port': '112.253.2.61:8080', 'user_pass': ''},
        {'ip_port': '61.135.217.12:80', 'user_pass': ''},
        {'ip_port': '61.135.217.17:80', 'user_pass': ''},
        {'ip_port': '111.206.190.156:80', 'user_pass': ''},
    ]
    
    config = {
      'user':'root',
      'password':'lixinxin',
      'host':'SpiderDb',
      'database':'qy_spider'
      }
    
    values = []
    
    def __init__(self, continent=None):
        
        # 最多抓5页
        # 涉及到线程安全的初始化，需要放到这里，比如redis需要用大洲来标识使用哪个集合
        self.current_continent = continent;
        
        self.connect_mysql() 
        
        
        
        # 查询大洲下目的地
        xcursor = self.cnx.cursor(dictionary=True)
        xcursor.execute("select max(travel_id) as mt from qy_comments")   # 查询已经获取的目的地评论，用来做增量式抓取
        _info = xcursor.fetchone()
        max_id = 0 
        if _info['mt'] :
            max_id = _info['mt']
            print 'continue from ' , max_id
        xcursor.execute("select id,travel_id,qy_pid from poi where travel_id>"+('%d' %max_id)+" order by travel_id asc") 
        poi_list = xcursor.fetchall()
        xcursor.close()
        
        for poi in poi_list :
            self.exec_get_comment(poi)

    
    def exec_get_comment(self, poi_info):
        
        print poi_info
        
        id_str = ('%d' %poi_info['id'])
        qy_pid_str = ('%d' %poi_info['qy_pid'])
        travel_id_str = ('%d' %poi_info['travel_id'])
        
        print travel_id_str , ' exec ... '
        
        proxy_list = self.PROXIES
        run = True
        page = 1
        
        max_page = 5
        req_time_limit = 3
        
        while run :

            if page > max_page :
                break;
            
            params = urlencode({
                                'page': page, 
                                'order': 5,
                                'poiid': poi_info['qy_pid'],
                                'starLevel': 'all'
                                })
            
            agent_index = int(random() * 1000) % len(self.USER_AGENTS)
            
            headers = {"Content-type": "application/x-www-form-urlencoded", 
                       "User-Agent": self.USER_AGENTS[agent_index] ,
                       "Accept": "text/plain"}
            
            proxy = ''
            proxy_index = -1
            if len(proxy_list) > 0 :
            
                proxy_index = int(random() * 1000) % len(proxy_list)
                
                proxy = 'http://' + proxy_list[proxy_index]['ip_port']
                #proxy = 'http://10.25.31.2:80' 
                opener = urllib2.build_opener( urllib2.ProxyHandler({'http':proxy}) )
                urllib2.install_opener( opener )
            else:
                opener = urllib2.build_opener( urllib2.ProxyHandler({}) )
                urllib2.install_opener( opener )
            
            req = urllib2.Request('http://place.qyer.com/poi.php?action=comment', params, headers)
            #req = urllib2.Request('http://123.56.255.62/xxoo.php', '', headers)
            
            json_str = ''
            try:
                self.log('request ' + travel_id_str + ' page ' + ('%d' %page) + ' use proxy ' + proxy)
                sContent = urllib2.urlopen(req, timeout=req_time_limit)
                json_str = sContent.read()
                #print json_str
            except (urllib2.URLError,socket.timeout) as ue:
                print str(ue) 
                if proxy != '' :
                    self.log('remove proxy ' + proxy)
                    self.PROXIES.remove(self.PROXIES[proxy_index])
                else:
                    run = False
                    # 没有可用代理，可能全部被屏蔽，退出程序，等待管理员更换ip
                    self.log('All proxies were baned, change proxies list please !')
                    exit()
                
                # 切换其他代理IP地址
                continue
            
            #保存到文件 & 写入数据库
            ok_flag = True
            self.log('found id ' + travel_id_str)
            
            # 保存到文件
            subpath = poi_info['id'] % 100
            _path = './comment_jsons/' + self.current_continent + '/' + ('%d' %subpath) + '/'  ;
            if not os.path.isdir(_path) :
                try:
                    os.makedirs(_path)
                except OSError:
                    self.log('create ' + _path + ' failed ')
                    ok_flag = False
                pass
            
            
            if ok_flag :
                _file = _path + travel_id_str + '_' + ('%d' %page) + '.json'
                
                try :
                    fp = open(_file, 'w')
                    fp.write( json_str )
                    fp.close()
                except IOError :
                    self.log('create ' + _path + ' failed ')
                    ok_flag = False
                pass
            
            # 更新status
            if ok_flag :
                isconn = self.cnx.is_connected()
                if not isconn :
                    self.log('connection is lose')
                    self.connect_mysql()
                now = int(time.time())
                xcursor = self.cnx.cursor()
                xcursor.execute("insert into qy_comments(`travel_id`, `qy_pid`, `addtime`, `page`, `filepath`) values("+travel_id_str+", "+qy_pid_str+", "+('%d' %now)+", "+('%d' %page)+", '"+_file+"')") 
                self.cnx.commit()
            else:
                self.log('filesystem err')
                exit()
            
            
            print travel_id_str , ' page ' , page, ' done ... '
            
            try:
                jsonobj = json.loads(json_str)
                #print jsonobj['data']['lists']
                if len(jsonobj['data']['lists']) <=0 :
                    # 没有数据了，退出循环
                    run = False
                    print 'no datas '
                    pass
            except:
                # 没有数据了，退出循环
                run = False
                print 'no datas '
                pass
            
            page = page + 1


    def connect_mysql(self):
        self.log('connection to ' + self.config['host'])
        self.cnx = mysql.connector.connect(**self.config)
        self.cnx.cursor().execute("set names utf8")
    
    def log(self, msg):
        
        print msg
        
        _path = './logs/getcomment/' + self.current_continent + '/' ;
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

    def _md5(self, _val):
        m2 = hashlib.md5()
        m2.update(_val)
        return m2.hexdigest().upper()
    

if len(sys.argv) < 2 :
    print 'usage : python getcomment.py Asialist'
    exit()

#  执行程序
getcomment(sys.argv[1])  

