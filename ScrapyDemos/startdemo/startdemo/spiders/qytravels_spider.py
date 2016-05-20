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
from cgi import log
reload(sys)

sys.setdefaultencoding('utf-8')


'''
     目的地数据抓取
    scrapy crawl qytravels -s LOG_LEVEL=INFO -a continent=Asialist   命令行传参，可以跑多个进程，每个进程负责自己大洲下的抓取
     参数 Africalist, Asialist, Europelist, NorthAmericalist, Oceanialist, SouthAmericalist
'''

class QytravelsSpider(BaseSpider):
    name = "qytravels"
    allowed_domains = ["qyer.com","localhost"]
    start_urls = [
                  #'http://place.qyer.com/tabriz/alltravel/'
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
        
        # 创建 redis 连接
        self.redisdb = redis.Redis('SpiderDb')
        # 初始化内存数据库
        self.redisdb.delete(self.set_url_sign_citys)
        self.redisdb.delete(self.set_url_sign_travels)
        
        # 创建mysql连接
        self.cnx = mysql.connector.connect(**self.config)
        self.cnx.cursor().execute("set names utf8")
        
        #初始化已经采集的列表地址
        xcursor = self.cnx.cursor()
        xcursor.execute("select DISTINCT referer_sign from travels where continent='"+self.current_continent+"'") 
        for (referer_sign) in xcursor:
            if len(referer_sign) > 0:
                self.redisdb.sadd(self.set_url_sign_citys, referer_sign[0])
            pass
        xcursor.close()
        
        # 查询大洲下国家
        xcursor = self.cnx.cursor()
        xcursor.execute("select id,url,sign,continent,en,name from citys where continent='"+self.current_continent+"' and status=0") 
        for (id,url,sign,continent,en,name) in xcursor:
            #self.start_urls.append(url.strip('/') + '/alltravel/')
            self.appendToUrls(url.strip('/') + '/alltravel/')
            pass
        xcursor.close()
        
        #初始化已存在目的地列表 url
        xcursor = self.cnx.cursor()
        xcursor.execute("select sign from travels where continent='"+self.current_continent+"'") 
        for (sign) in xcursor:
            if len(sign) > 0:
                self.redisdb.sadd(self.set_url_sign_travels, sign[0])
            pass
        xcursor.close()
        
        pass

    def parse(self, response):
        
        referer = response.url
        self.log("exec city url is "+referer)
        
        print "exec city url is "+referer
        
        if referer.endswith('alltravel/') or  referer.endswith('alltravel') :
    
            ''' 处理分页，仅主页处理 '''
            
            pages = response.css('#poiListPage div.ui_page a').xpath('@data-page').extract()
            
            maxpage = 1
            if len(pages) > 0 :
                for _page in pages :
                    _pn = self.parseInt(_page)
                    maxpage = max([maxpage, _pn])
            else:
                self.log('city '+referer+' no page') 
                print 'city '+referer+' no page'
            
            if maxpage > 1 :
                for _i in range(1, maxpage) :
                    _pn = _i+1
                    self.appendToUrls( referer + '?page=' + ('%d' %_pn) )    # 将分页子页面添加到抓取队列
                    pass
                pass
        
        
        ''' 处理POI列表 '''
        poiurls_selector = response.css('#poiLists li')
        clist = []
        for _poi_selector  in poiurls_selector:
            _data = dict()
            _img = _poi_selector.css('p.pics img').xpath('@src').extract()
            _name =  _poi_selector.css('h3.title a').xpath('text()[1]').extract()
            _en = _poi_selector.css('h3.title a span').xpath('text()').extract()
            _link = _poi_selector.css('h3.title a').xpath('@href').extract()
            
            if len(_link)>0 and len(_name)>0 :
                _data['link'] = _link.pop().replace("'", "\\'").strip()
                _data['name']  = _name.pop().replace("'", "\\'").strip()
                _data['referer'] = referer.replace("'", "\\'").strip()
                _data['img'] = ''
                _data['en'] = ''
                
                if len(_img) > 0:
                    _data['img'] = _img.pop().replace("'", "\\'").strip()
                if len(_en) > 0:
                    _data['en'] = _en.pop().replace("'", "\\'").strip()

                #写数据库
                clist.append(_data)
            
        if len(clist) > 0 :
            self.process_clist(clist)
        
        clist = []  # reset
        print referer + ' complete !'
        
    def parseInt(self, _num_str):
        
        '''
        转换成 int 类型
        @param _num_str: 字符串类型
        @return: 成功返回数组类型值，失败返回 -1
        '''
        
        _num_str = _num_str.strip()
        
        num = -1
    
        try:
            num = int(_num_str)
        except ValueError:
            num = -1
            pass
        
        return num
             
    def process_clist(self, clist):
        
        counter_i = 0
        
        for i in clist :
            hashstr = self._md5(i['link'])
            if self.redisdb.sismember(self.set_url_sign_travels, hashstr):
                continue  # 当url已存在，则不需添加
            
            self.redisdb.sadd(self.set_url_sign_travels, hashstr)
            
            now = int(time.time())
            referer_hashstr = self._md5(i['referer'])
            
            _continent = self.current_continent.replace("'", "\'")
            self.values.append("('"+i['name']+"', '"+i['en']+"', "+('%d' %now)+", '"+_continent+"', '"+i['referer']+"', 0, '"+i['link']+"', '"+hashstr+"', '"+referer_hashstr+"', '"+i['img']+"')")
            
            counter_i = counter_i+1
            if counter_i % 100 == 0 :
                self.flush_data()
            
        self.flush_data()
    
    def flush_data(self):
        xcursor = self.cnx.cursor()
        if len(self.values) > 0 :
            _values = ",".join(self.values)
            
            xcursor.execute("insert into travels(name, en, createtime, continent, referer, status, url, sign, referer_sign, img) values"+_values)
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
        
        self.log('added sub page ' + url)
        
        sign = self._md5(url)
        if self.redisdb.sismember(self.set_url_sign_citys, sign):
            return  # 当url已存在，则不需添加
        
        self.redisdb.sadd(self.set_url_sign_citys, sign)
        self.start_urls.append(url) 
        return
    
    def _md5(self, _val):
        m2 = hashlib.md5()
        m2.update(_val)
        return m2.hexdigest().upper()
    
    