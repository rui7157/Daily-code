# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HospitalItem(scrapy.Item):
    
    hospitalName=scrapy.Field()
    hospitalAddress=scrapy.Field()
    hospitalPhoneNumber=scrapy.Field()
    hospitalLevel=scrapy.Field()
    hospitalType=scrapy.Field()
    hospitalFaxNumber=scrapy.Field()
    hospitalEmail=scrapy.Field()
    hospitalWebsite=scrapy.Field()
    hospitalProvince=scrapy.Field()