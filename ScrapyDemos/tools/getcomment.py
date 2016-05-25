# -*- coding: utf-8 -*-
import urllib2
from urllib import urlencode
from random import random
import mysql.connector
import os
import time
import hashlib
import sys

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
        #{'ip_port': '119.188.94.145:80', 'user_pass': ''},
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
        
        # 涉及到线程安全的初始化，需要放到这里，比如redis需要用大洲来标识使用哪个集合
        self.current_continent = continent;
    
        params = urlencode({
                            'page': 1, 
                            'order': 5,
                            'poiid': 568613,
                            'starLevel': 'all'
                            })
        
        agent_index = int(random() * 1000) % len(self.USER_AGENTS)
        
        headers = {"Content-type": "application/x-www-form-urlencoded", 
                   "User-Agent": self.USER_AGENTS[agent_index] ,
                   "Accept": "text/plain"}
        
        proxy_index = int(random() * 1000) % len(self.PROXIES)
        
        proxy = 'http://' + self.PROXIES[proxy_index]['ip_port']
        print proxy
        opener = urllib2.build_opener( urllib2.ProxyHandler({'http':proxy}) )
        urllib2.install_opener( opener )
        
        req = urllib2.Request('http://place.qyer.com/poi.php?action=comment', params, headers)
        # req = urllib2.Request('http://123.56.255.62/xxoo.php', '', headers)
        sContent = urllib2.urlopen(req, timeout=3)
        print sContent.read()
        
    
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
    

# if len(sys.argv) < 2 :
#     print 'usage : python getcomment.py Asialist'
#     exit()

#  执行程序
# getcomment(sys.argv[1])  
getcomment('Asialist')  

