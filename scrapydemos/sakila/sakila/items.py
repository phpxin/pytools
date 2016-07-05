# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SakilaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FilmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    last_update = scrapy.Field()
    replacement_cost = scrapy.Field()
    referer = scrapy.Field()
    pass