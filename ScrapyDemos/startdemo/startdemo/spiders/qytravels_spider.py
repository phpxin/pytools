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

import sys
reload(sys)

sys.setdefaultencoding('utf-8')


'''
     城市数据抓取
     scrapy crawl qycitys -s LOG_LEVEL=INFO -a continent=Asialist   命令行传参，可以跑多个进程，每个进程负责自己大洲下的抓取
     参数 Africalist, Asialist, Europelist, NorthAmericalist, Oceanialist, SouthAmericalist
'''

class QytravelsSpider(BaseSpider):
    name = "qytravels"
    allowed_domains = ["qyer.com","localhost"]
    start_urls = [
    ]
    
    qy_host = 'http://place.qyer.com'
    
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
        self.set_url_sign_citys = 'set_url_sign_citys_' + continent       #redis 集合 已获取的城市指纹，用来去重   md5("http://place.qyer.com/pyongyang/")
        self.set_url_sign_travels = 'set_url_sign_travels_' + continent #redis 集合，目的地列表 url 指纹    md5("http://place.qyer.com/manama/alltravel/")
        
        # 创建mysql连接
        self.cnx = mysql.connector.connect(**self.config)
        self.cnx.cursor().execute("set names utf8")
        # 查询大洲下国家
        
        xcursor = self.cnx.cursor()
        xcursor.execute("select id,url,sign,continent,en,name from citys where continent='"+self.current_continent+"' and status=0") 
        for (id,url,sign,continent,en,name) in xcursor:
            self.start_urls.append(url.strip('/') + '/alltravel/')
            pass
        xcursor.close()
        
        
        # 创建 redis 连接
        self.redisdb = redis.Redis('SpiderDb')
        # 初始化内存数据库
        self.redisdb.delete(self.set_url_sign_citys)
        self.redisdb.delete(self.set_url_sign_travels)
        
        #初始化已存在city url
        xcursor = self.cnx.cursor()
        xcursor.execute("select sign from travels where continent='"+self.current_continent+"'") 
        for (sign) in xcursor:
            self.redisdb.sadd(self.set_url_sign_travels, sign)
            pass
        xcursor.close()
        
        pass

    def parse(self, response):
        
        referer = response.url
        self.log("exec country url is "+referer)
        
        print "exec country url is "+referer

        ''' 处理分页 '''
        
        hrefs = response.css('a.ui_page_item').xpath('@href').extract()
        
        # 有值 [u'/algeria/citylist-0-0-1/', u'/algeria/citylist-0-0-2/', u'/algeria/citylist-0-0-2/']
        # 无值 []
        if len(hrefs) > 0 :
            for href in hrefs :
                self.appendToUrls(self.qy_host + href)
                
        
        ''' 处理城市列表 '''
        
        cityurls_selector = response.css('ul.plcCitylist li')
        clist = []
        for _city_selector  in cityurls_selector:
            _data = dict()
            _img = _city_selector.css('p.pics img').xpath('@src').extract()
            _name =  _city_selector.css('h3.title a').xpath('text()[1]').extract()
            _en = _city_selector.css('h3.title a span.en').xpath('text()').extract()
            _link = _city_selector.css('h3.title a').xpath('@href').extract()
            
            if len(_link)>0 and len(_name)>0 :
                _data['img'] = _img.pop().replace("'", "\\'")
                _data['name']  = _name.pop().replace("'", "\\'")
                _data['en'] = _en.pop().replace("'", "\\'")
                _data['link'] = _link.pop().replace("'", "\\'")
                _data['referer'] = referer.replace("'", "\\'")

                #写数据库
                clist.append(_data)
        
        if len(clist) > 0 :
            self.process_clist(clist)
        
        clist = []  # reset
        
        print referer + ' complete !'
             
    def process_clist(self, clist):
        
        counter_i = 0
        
        for i in clist :
            hashstr = self._md5(i['link'])
            if self.redisdb.sismember(self.set_url_sign_citys, hashstr):
                continue  # 当url已存在，则不需添加
            
            self.redisdb.sadd(self.set_url_sign_citys, hashstr)
            
            now = int(time.time())
            _continent = self.current_continent.replace("'", "\'")
            self.values.append("('"+i['link']+"', '"+hashstr+"', '"+_continent+"', "+('%d' %now)+", '"+i['en']+"', 0, '"+i['name']+"', '"+i['referer']+"', '"+i['img']+"')")
            
            counter_i = counter_i+1
            if counter_i % 100 == 0 :
                self.flush_data()
            
        self.flush_data()
    
    def flush_data(self):
        xcursor = self.cnx.cursor()
        if len(self.values) > 0 :
            _values = ",".join(self.values)
            
            xcursor.execute("insert into citys(url, sign, continent, createtime, en, status, name, referer, img) values"+_values)
            self.cnx.commit()
            pass
        xcursor.close()
        self.values = []
        return
    
    def log(self, msg):
        
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
        
        sign = self._md5(url)
        if self.redisdb.sismember(self.set_url_sign_countrys, sign):
            return  # 当url已存在，则不需添加
        
        self.redisdb.sadd(self.set_url_sign_countrys, sign)
        
        self.start_urls.append(url) 
    
    def _md5(self, _val):
        m2 = hashlib.md5()
        m2.update(_val)
        return m2.hexdigest().upper()
    
    