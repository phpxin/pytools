# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class StartdemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    link = Field()
    desc = Field()
    pass

class QyCountrysItem(scrapy.Item):
    title = Field()
    en = Field()
    link = Field()
    parent = Field() #所属大洲
    pass