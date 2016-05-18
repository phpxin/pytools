# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
import mysql.connector
from mysql.connector import connect, Connect
from datetime import time
import hashlib
'''

from startdemo.items import QyCountrysItem

class StartdemoPipeline(object):
    def process_item(self, item, spider):
        return item


class QyCountrysPipeline(object):
    
    '''
    config = {
          'user':'root',
          'password':'lixinxin',
          'host':'127.0.0.1',
          'database':'qy_spider'
          }
    
    values = []
    def __init__(self):
        self.cnx = mysql.connector.connect(**self.config)
        self.cnx.execute("set names utf8")
        print 'a>>>>////'
        print self.cnx
    '''
    def process_item(self, item, spider):
        
        #print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        #print item
        '''
        for i in item :
            now = int(time.time())
            
            m2 = hashlib.md5()   
            m2.update(i['link'])
            hashstr = m2.hexdigest().upper()
            self.values.append("('"+i['link']+"', '"+hashstr+"', '"+i['parent']+"', "+now+", '"+i['en']+"', 0, '"+i['title']+"')")
            break;
        
        self.flush_data()
        '''
        #return item
    
        '''
    def flush_data(self):
        self.cnx = mysql.connector.connect({
          'user':'root',
          'password':'lixinxin',
          'host':'127.0.0.1',
          'database':'qy_spider'
          })
        print "\n", self.cnx, "\n"
        print 'aaabbb'
        self.cnx.execute("set names utf8")
        if len(self.values) > 0 :
            _values = ",".join(self.values)
            self.cnx.execute("insert into countrys(url, sign, continent, createtime, en, status, name) values"+_values)
            pass
        self.values = []
        self.cnx.close()
        return
        '''
    
    