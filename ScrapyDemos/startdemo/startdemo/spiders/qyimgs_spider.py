# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider

import mysql.connector
import time
import hashlib
import redis
import os



'''
     图片数据抓取
    scrapy crawl qyimgs -s LOG_LEVEL=INFO -a continent=Asialist   命令行传参，可以跑多个进程，每个进程负责自己大洲下的抓取
     参数 Africalist, Asialist, Europelist, NorthAmericalist, Oceanialist, SouthAmericalist
'''

class QytravelsSpider(BaseSpider):
    name = "qyimgs"
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
        self.set_url_sign_travels = 'set_url_sign_travels_' + continent #redis 集合，目的地列表 url 指纹    md5("http://place.qyer.com/manama/alltravel/")
        self.set_url_sign_imgs = 'set_url_sign_imgs_' + continent       #redis 集合 已获取的图片url指纹
        
        # 创建 redis 连接
        self.redisdb = redis.Redis('SpiderDb')
        # 初始化内存数据库
        self.redisdb.delete(self.set_url_sign_imgs)
        self.redisdb.delete(self.set_url_sign_travels)
        
        # 创建mysql连接
        self.connect_mysql()
        
        #初始化已经采集的列表地址
        xcursor = self.cnx.cursor()
        xcursor.execute("select DISTINCT referer_sign from imgs_"+self.current_continent.lower()+" where continent='"+self.current_continent+"'") 
        for (referer_sign) in xcursor:
            if len(referer_sign) > 0:
                print referer_sign[0]
                self.redisdb.sadd(self.set_url_sign_travels, referer_sign[0])
            pass
        xcursor.close()
        
        # 查询大洲下目的地
        xcursor = self.cnx.cursor()
        xcursor.execute("select id,url,sign,continent,en,name from travels where continent='"+self.current_continent+"' ") 
        for (id,url,sign,continent,en,name) in xcursor:
            self.appendToUrls(url.strip('/') + '/photo/')
            pass
        xcursor.close()
        
        #初始化已存在图片列表 url
        xcursor = self.cnx.cursor()
        xcursor.execute("select sign from imgs_"+self.current_continent.lower()+" where continent='"+self.current_continent+"'") 
        for (sign) in xcursor:
            if len(sign) > 0:
                self.redisdb.sadd(self.set_url_sign_imgs, sign[0])
            pass
        xcursor.close()
        
        pass

    def parse(self, response):
        referer = response.url
        self.log("exec city url is "+referer)
        
        ''' 处理图片列表 '''
        imgurls_selector = response.css('ul.pla_photolist li')
        clist = []
        for _img_selector  in imgurls_selector:
            _data = dict()
            _img = _img_selector.css('p.pic img').xpath('@src').extract()
            
            if len(_img)>0 :
                _data['url'] = _img.pop().replace("'", "\\'").strip()
                _data['referer'] = referer.replace("'", "\\'").strip()
                print _data

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
            hashstr = self._md5(i['url'])
            if self.redisdb.sismember(self.set_url_sign_imgs, hashstr):
                continue  # 当url已存在，则不需添加
            
            self.redisdb.sadd(self.set_url_sign_travels, hashstr)
            
            now = int(time.time())
            referer_hashstr = self._md5(i['referer'])
            
            _continent = self.current_continent.replace("'", "\'")
            self.values.append("('"+i['url']+"', "+('%d' %now)+", '"+_continent+"', '"+hashstr+"', '"+i['referer']+"', '"+referer_hashstr+"')")
            
            counter_i = counter_i+1
            if counter_i % 100 == 0 :
                self.flush_data()
            
        self.flush_data()
        
    def connect_mysql(self):
        self.log('connection to ' + self.config['host'])
        self.cnx = mysql.connector.connect(**self.config)
        self.cnx.cursor().execute("set names utf8")
    
    def flush_data(self):
        
        isconn = self.cnx.is_connected()
        if not isconn :
            self.log('connection is lose')
            self.connect_mysql()
            
        xcursor = self.cnx.cursor()
        if len(self.values) > 0 :
            _values = ",".join(self.values)
            xcursor.execute("insert into imgs_" + self.current_continent.lower() + "(url, createtime, continent, sign, referer, referer_sign) values"+_values)
            self.cnx.commit()
            pass

        xcursor.close()
        self.values = []
        return
    
    def log(self, msg):
        
        print msg
        
        _path = './logs/imgs/' + self.current_continent + '/' ;
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
        if self.redisdb.sismember(self.set_url_sign_travels, sign):
            return  # 当url已存在，则不需添加
        
        self.redisdb.sadd(self.set_url_sign_travels, sign)
        self.start_urls.append(url) 
        return
    
    def _md5(self, _val):
        m2 = hashlib.md5()
        m2.update(_val)
        return m2.hexdigest().upper()
    
    