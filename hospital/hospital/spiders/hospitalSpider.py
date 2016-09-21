# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
import re
import urllib
from hospital.items import HospitalItem

"""
爬取医院信息存入MySQLs数据库
"""

class HospitalspiderSpider(CrawlSpider):
    name = 'hospitalSpider'
    allowed_domains = ['a-hospital.com']
    start_urls = ['http://www.a-hospital.com/w/%E5%85%A8%E5%9B%BD%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8',]
    
    def start_requests(self):
        yield Request(url=self.start_urls[0],callback=self.parse_item0)
    
    def parse_item0(self,response):
        provinceUrlList=re.findall(r'<b><a href="(/w/.*?)" title=".*?">.*?</a></b>',response.body)
        for url in provinceUrlList:
            yield Request(url="http://www.a-hospital.com{}".format(url),callback=self.parse_item)


    def parse_item(self, response):
        i = HospitalItem()  #http://www.a-hospital.com/w/%E5%9B%9B%E5%B7%9D%E7%9C%81%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8
        province=urllib.unquote(response.url[len("http://www.a-hospital.com/w/"):])
        for name,content in re.findall(r'<li><b><a href=".*?" title=".*?">(.*?)</a>.*?</b>[\s\S]*?<ul>([\s\S]*?)</ul>[\s\S]*?</li>',response.body):
            i['hospitalName'] = name.decode('utf-8')
            content=content.decode("utf-8")
            hospitalAddress=re.findall(u"<b>医院地址</b>[:|：](.*?)</li>",content)
            hospitalPhoneNumber= re.findall(u"<b>联系电话</b>[:|：](.*?)</li>",content)
            hospitalLevel = re.findall(u"<b>医院等级</b>[:|：](.*?)</li>",content)
            hospitalType=re.findall(u"<b>经营方式</b>[:|：](.*?)</li>",content)
            hospitalFaxNumber=re.findall(u"<b>传真号码</b>[:|：](.*?)</li>",content)
            hospitalEmail= re.findall(u"<b>电子邮箱</b>[:|：](.*?)</li>",content)
            hospitalWebsite= re.findall(u'<b>医院网站</b>[:|：]<a href="(.*?)" class="external free" rel="nofollow" target="_blank">.*?</a></li>',content)
            if hospitalAddress:
                i["hospitalAddress"]=hospitalAddress[0]
            if hospitalPhoneNumber:
               i['hospitalPhoneNumber']= hospitalPhoneNumber[0]
            if hospitalLevel:
                i['hospitalLevel']=hospitalLevel[0]
            if hospitalType:
                i['hospitalType']=hospitalType[0]
            if hospitalFaxNumber:
                i['hospitalFaxNumber']=hospitalFaxNumber[0]
            if hospitalEmail:
                i['hospitalEmail']=hospitalEmail[0]
            if hospitalWebsite:
                i['hospitalWebsite']=hospitalWebsite[0]
            i['hospitalProvince']=province.decode('utf-8')
            yield i