# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy import crawler

import mysql.connector
from mysql.connector import connect, Connect
import time
import hashlib
import redis
import os
from _codecs import decode



'''
     目的地html页面下载
    scrapy crawl qydownload -s LOG_LEVEL=INFO -a continent=Asialist   命令行传参，可以跑多个进程，每个进程负责自己大洲下的抓取
     参数 Africalist, Asialist, Europelist, NorthAmericalist, Oceanialist, SouthAmericalist
'''

class QydownloadSpider(BaseSpider):
    name = "qydownload"
    allowed_domains = ["qyer.com","localhost"]
    start_urls = [
                  #'http://place.qyer.com/tabriz/alltravel/'
    ]
    
    continents = ['Asialist', 'Europelist', 'Africalist', 'NorthAmericalist', 'SouthAmericalist', 'Oceanialist', 'Antarcticalist']
    
    current_continent = ''     # Asialist, Europelist, Africalist, NorthAmericalist, SouthAmericalist, Oceanialist, Antarcticalist
    
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

        # 创建mysql连接
        self.connect_mysql()
        
        # 查询大洲下目的地
        xcursor = self.cnx.cursor()
        xcursor.execute("select id,url,sign,continent from travels where continent='"+self.current_continent+"' and status=0") 
        for (id,url,sign,continent) in xcursor:
            self.appendToUrls(url)
            pass
        xcursor.close()

        pass
    
    def parse(self, response):
        
        referer = response.url
        
        self.log("exec city url is "+referer)
        
        isconn = self.cnx.is_connected()
        if not isconn :
            self.log('connection is lose')
            print 'connection is lose'
            self.connect_mysql()
            pass
        
        urlsign = self._md5(referer)
        xcursor = self.cnx.cursor(dictionary=True)
        xcursor.execute("select id from travels where continent='"+self.current_continent+"' and sign='"+urlsign+"' ") 
        
        info = xcursor.fetchone()
        
        if info :
            
            ok_flag = True
            _id = int(info['id'])
            _id_str = '%s' %info['id']
            
            self.log('found id ' + _id_str)
            
            
            # 保存到文件
            subpath = _id % 100
            _path = './travel_htmls/' + self.current_continent + '/' + ('%d' %subpath) + '/' ;
            if not os.path.isdir(_path) :
                try:
                    os.makedirs(_path)
                except OSError:
                    self.log('create ' + _path + ' failed ')
                    ok_flag = False
                pass
            
            
            if ok_flag :
                _file = _path + _id_str + '.html'
                
                try :
                    fp = open(_file, 'w')
                    fp.write( response.body )
                    fp.close()
                except IOError :
                    self.log('create ' + _path + ' failed ')
                    ok_flag = False
                pass
            
            # 更新status
            if ok_flag :
                xcursor.execute("update travels set status=1,filepath='" + _file + "' where id=" + _id_str + " ") 
            else:
                xcursor.execute("update travels set status=2 where id=" + _id_str + " ") 
            
            
            print referer + ' complete !'
        else:
            self.log(referer + ' not in table !')
            
        xcursor.close()

        
    def connect_mysql(self):
        self.log('connection to ' + self.config['host'])
        self.cnx = mysql.connector.connect(**self.config)
        self.cnx.cursor().execute("set names utf8")
    
    def log(self, msg):
        
        print msg
        
        _path = './logs/' + self.current_continent + '/' ;
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

    def appendToUrls(self, url):
        
        self.log('added page ' + url)
        self.start_urls.append(url) 
        
        return
    
    def _md5(self, _val):
        m2 = hashlib.md5()
        m2.update(_val)
        return m2.hexdigest().upper()
    
    