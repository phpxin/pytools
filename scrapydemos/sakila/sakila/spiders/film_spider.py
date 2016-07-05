# -*- coding: utf-8 -*-
from scrapy.spiders import BaseSpider
from scrapy.loader import ItemLoader
from sakila.items import FilmItem
import re
from scrapy import Request

import mysql.connector
from mysql.connector import connect, Connect
import time

class FilmSpider(BaseSpider):
    name = "film"
    allowed_domains = ["laravel.test.com"]
    start_urls = [
        "http://laravel.test.com/sakila/list",
    ]

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

    def parse(self, response):
        
        if response.url == 'http://laravel.test.com/sakila/list' :
            '''
            film_list_dom = response.css('table.list tr')
            
            film_list = []
            item = FilmItem()
            for item_dom in film_list_dom :
                contents = item_dom.css('td').xpath('text()').extract()
                if len(contents) > 0 :
                    
                    item['replacement_cost'] = contents.pop()
                    item['last_update'] = contents.pop()
                    item['description'] = contents.pop()
                    item['title'] = contents.pop()
                    film_list.append(item)
            '''
            reqs = []
            film_list_dom = response.css('table.list tr td a').xpath('@href').extract()
            now = int(time.time())
            for url in film_list_dom :
                _url = 'http://laravel.test.com' + url 
                self.cnx.cursor().execute("insert into list(`url`, `referer`, `addtime`) values('"+_url+"', '"+response.url+"', "+('%d' %now)+")")
                self.cnx.commit()
                
                # 构建一个请求并添加到需要返回的请求字典中
                reqs.append(Request(_url, self.parse))
            
            return reqs
        
        elif re.compile('http\:\/\/laravel\.test\.com\/sakila\/detail\/\d+', re.IGNORECASE|re.MULTILINE).match(response.url) :
            title = response.css('#title').xpath('text()').extract()
            description = response.css('#description').xpath('text()').extract()
            replacement_cost = response.css('#replacement_cost').xpath('text()').extract()
            last_update = response.css('#last_update').xpath('text()').extract()
            
            item = FilmItem()
            item['referer'] = response.url
            
            if len(title) > 0 :
                item['title'] = title.pop()
            else:
                return 
            
            if len(description) > 0 :
                item['description'] = description.pop()
            if len(replacement_cost) > 0 :
                item['replacement_cost'] = replacement_cost.pop()
            if len(last_update) > 0 :
                item['last_update'] = last_update.pop()
            
            #返回一个 FilmItem 对象，可以触发FilmPipeline
            return item
        
        else:
            # 不支持的来源
            pass
        