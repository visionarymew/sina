# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SinaItem(scrapy.Item):
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()

    sonUrls = scrapy.Field()
    head = scrapy.Field()
    content = scrapy.Field()
    savepath = scrapy.Field()