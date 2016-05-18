# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider

class UthingSpider(BaseSpider):
    name = "uthing"
    allowed_domains = ["uthing.cn"]
    start_urls = [
        "http://www.uthing.cn",
    ]

    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #filename = 'test.html' 
        #open(filename, 'wb').write(response.body)
        li = response.selector.xpath('//img/@src').extract()
        print li
        