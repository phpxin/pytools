# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import mysql.connector
from mysql.connector import connect, Connect
import time

class SakilaPipeline(object):
    def process_item(self, item, spider):
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>pipelines is called'
        print item
        return item


class FilmPipeline(object):
    
    config = {
        'user':'root',
        'password':'lixinxin',
        'host':'127.0.0.1',
        'database':'scrapydemo'
        }
    
    def __init__(self):
        self.connect_mysql()
        return

    def connect_mysql(self):
        print 'connection to ' + self.config['host']
        self.cnx = mysql.connector.connect(**self.config)
        self.cnx.cursor().execute("set names utf8")   
    
    def process_item(self, item, spider):
        #print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>pipelines is called'
        print "save " , item['title']
        
        now = int(time.time())
        self.cnx.cursor().execute("insert into detail(`title`, `description`, `last_update`, `replacement_cost`, `referer`, `addtime`) \
                                    values('"+item['title']+"', '"+item['description']+"', '"+item['last_update']+"', '"+item['replacement_cost']+"', '"+item['referer']+"', "+('%d' %now)+")")
        self.cnx.commit()
        
        return item