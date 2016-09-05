# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnfeolItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    type = scrapy.Field()
    min_price = scrapy.Field()
    max_price = scrapy.Field()
    change = scrapy.Field()
    unit = scrapy.Field()
    remark = scrapy.Field()
    date = scrapy.Field()
    pass
