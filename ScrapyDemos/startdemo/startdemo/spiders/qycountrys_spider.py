# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
#from pywin.dialogs.login import title
from startdemo.items import QyCountrysItem

'''

穷游国家列表解析 http://place.qyer.com/
scrapy crawl qycountrys -s LOG_LEVEL=INFO

'''

import mysql.connector
from mysql.connector import connect, Connect
import time
import hashlib

class QycountrysSpider(BaseSpider):
    name = "qycountrys"
    allowed_domains = ["localhost"]
    start_urls = [
        "http://localhost/Demos/qyfx/qy_countrys.html",
    ]
    
    continents = ['Asialist', 'Europelist', 'Africalist', 'NorthAmericalist', 'SouthAmericalist', 'Oceanialist', 'Antarcticalist']
    
    config = {
          'user':'root',
          'password':'lixinxin',
          'host':'SpiderDb',
          'database':'qy_spider'
          }
    
    values = []
    
    def __init__(self):
        self.cnx = mysql.connector.connect(**self.config)
        self.cnx.cursor().execute("set names utf8")

    def parse(self, response):
        
        for _continent in self.continents :
        
            clist = []   #QyCountrysItem
            #print _continent
            #asia_sel = response.selector.xpath('//*[@id="'+_continent+'"]')
            
            #print asia_sel
            
            #_item = response.selector.xpath('//*[@id="'+_continent+'"]/div/ul/li/a')    # 必须按照层级写，遵守DOM xpath标准
            _item = response.css('#'+_continent+' ul li a')
            #print _item
            for a_sel_i in _item:
                href = a_sel_i.xpath('@href').extract()
                title = a_sel_i.xpath('text()').extract()
                en = a_sel_i.xpath('*[@class="en"]/text()').extract()
                
                if len(href)>0 and len(title)>0 :
                    _qc = QyCountrysItem()
                    _qc['title'] = title.pop()
                    _qc['link'] = href.pop()
                    _qc['en'] = ''
                    if len(en)>0 :
                        _qc['en'] = en.pop()
                        pass
                    _qc['parent'] = _continent
                    clist.append(_qc);
                    pass
                pass
                
            
            if len(clist) > 0 :
                self.process_clist(clist)
            #print clist
            clist = []  # reset
            pass

    def process_clist(self, clist):
        
        for i in clist :
            now = int(time.time())
            
            m2 = hashlib.md5()   
            m2.update(i['link'])
            hashstr = m2.hexdigest().upper()
            self.values.append("('"+i['link']+"', '"+hashstr+"', '"+i['parent']+"', "+('%d' %now)+", '"+i['en']+"', 0, '"+i['title']+"')")
            
        
        self.flush_data()
    
    def flush_data(self):
        xcursor = self.cnx.cursor()
        if len(self.values) > 0 :
            _values = ",".join(self.values)
            xcursor.execute("insert into countrys(url, sign, continent, createtime, en, status, name) values"+_values)
            pass
        self.values = []
        return
                