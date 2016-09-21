#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-17 14:17:42
# @Author  : NvRay (nvray@foxmail.com)


import os
from WapSinaWeiboLogin import Request
from lxml import etree
import re
from items import SinaWeiboItem
from db import dbconn
from functools import partial


dbconn.connect()
conn = dbconn.getConn()
sina_info=conn['sina'].info

class BaseSpider(object):
    pass

class WeiboSpider(BaseSpider):
    start_url = ["http://weibo.cn/5503137786/fans"]

    def __init__(self):
        super(BaseSpider, self).__init__()

    def parse(self, response):
        # 解析response yield link
        if not response:
            return None
        et = etree.HTML(response)      
        links = et.xpath("//*[@valign='top'][1]/a/@href")
        urls=[]
        for link in links:
            #根据id对每个用户信息入库
            print link
            uid=re.findall(r"http://weibo\.cn/u/(\w*)", link) #认证微信号格式不同（eq:http://weibo.cn/renzhenghao)
            if uid:
                uid=uid[0]
            else:
                continue   
            SinaWeiboItem["uid"]=uid   
            info_url = "http://weibo.cn/{uid}/info".format(uid=uid)
            Request(info_url, callback=self.parse_info)
            datas={"uid":SinaWeiboItem["uid"],"name":SinaWeiboItem["name"],"info":SinaWeiboItem["info"]}
            print sina_info.insert(datas)
            urls.append("http://weibo.cn/{uid}/fans".format(uid=uid)) #url返回开始下次执行
        return urls 
                                                                          

    def parse_info(self, response):
        et = etree.HTML(response)
        info = et.xpath("//*[@class='c'][3]/text()")
        SinaWeiboItem["name"]=info[0]
        SinaWeiboItem["info"]=info
        for i in info:
            print i.encode("gbk",'ignore')
        print "*"*30



if __name__ == "__main__":
    parse = WeiboSpider().parse
    url_seed=WeiboSpider.start_url
    
    def is_duplication(url,db_uid):
        
        uid=re.findall(r"http://weibo\.cn/(\w*)/info", url)[0].decode("gbk")
        print "{uid} in {db_uid}".format(uid=uid,db_uid=db_uid) 
        if uid in db_uid:
            return False
        else:
            return True

    def start(urls):
        url_pool=[]
        # new_urls=parse(response=Request(urls[0]))
        for url in urls:
            new_urls=parse(response=Request(url))
            db_uid=sina_info.distinct('uid')
            p_is_duplication=partial(is_duplication,db_uid=sina_info.distinct('uid'))
            for u in new_urls:
                url_pool.append(u)
        print url_pool
        return start(set(url_pool))

    start(url_seed)

