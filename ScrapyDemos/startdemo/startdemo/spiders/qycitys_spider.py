# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy import crawler

import mysql.connector
from mysql.connector import connect, Connect
import time
import hashlib

class QycitysSpider(BaseSpider):
    name = "qycitys"
    allowed_domains = ["qyer.com","localhost"]
    start_urls = [
        #"http://localhost/Demos/qyfx/cityindex.html",
        #"http://place.qyer.com/antarctica/citylist-0-0-1/",
        #"http://place.qyer.com/algeria/citylist-0-0-1/",
    ]
    
    qy_host = 'http://place.qyer.com'
    
    continents = ['Asialist', 'Europelist', 'Africalist', 'NorthAmericalist', 'SouthAmericalist', 'Oceanialist', 'Antarcticalist']
    
    current_continent = ''     # Asialist, Europelist, Africalist, NorthAmericalist, SouthAmericalist, Oceanialist, Antarcticalist
    
    citysigns = []    #已获取的城市指纹，用来去重
    
    config = {
          'user':'root',
          'password':'lixinxin',
          'host':'127.0.0.1',
          'database':'qy_spider'
          }
    
    def __init__(self, continent=None):
        #scrapy crawl qycitys -s LOG_LEVEL=INFO -a continent=Asia   命令行传参，可以跑多个进程，每个进程负责自己大洲下的抓取
        #'Asialist', 'Europelist', 'Africalist', 'NorthAmericalist', 'SouthAmericalist', 'Oceanialist', 'Antarcticalist'
        #print continent
        
        self.current_continent = continent;
        
        self.cnx = mysql.connector.connect(**self.config)
        self.cnx.cursor().execute("set names utf8")
        xcursor = self.cnx.cursor()
        
        # 查询大洲下国家
        xcursor.execute("select id,url,sign,continent,en,name from countrys where continent='"+self.current_continent+"' and status=0 limit 1") 
        for (id,url,sign,continent,en,name) in xcursor:
            #print(id,url,sign,continent,en,name)
            self.start_urls.append(url.strip('/') + '/citylist-0-0-1/')
   
        xcursor.close()
        pass

    def parse(self, response):
        hrefs = response.css('a.ui_page_item').xpath('@href').extract()
        #print  'a'      
        # 有值 [u'/algeria/citylist-0-0-1/', u'/algeria/citylist-0-0-2/', u'/algeria/citylist-0-0-2/']
        # 无值 []
        if len(hrefs) > 0 :
            for href in hrefs :
                #print self.qy_host + href
                self.start_urls.append(self.qy_host + href) 
        print self.start_urls
    
    
    
    