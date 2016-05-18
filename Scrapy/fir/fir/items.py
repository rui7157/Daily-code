# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FirItem(scrapy.Item):
	title=scrapy.Field()
	link=scrapy.Field()
	sesc=scrapy.Field()
