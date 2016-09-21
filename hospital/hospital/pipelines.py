# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from items import HospitalItem
from twisted.enterprise import adbapi
import datetime
import sys

class HospitalPipeline(object):


    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('pymysql',host='127.0.0.1', db='hospitalinfo',
                user='root', passwd='', cursorclass=pymysql.cursors.DictCursor,
                charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
  
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
  
        return item
  
    def _conditional_insert(self, tx, item):
        # create record if doesn't exist.
        # all this block run on it's own thread
        if isinstance(item,HospitalItem):
            # try:
                # 执行sql语句，插入记录
            k=[]
            v=[]
            for key,value in item.items():
                k.append("`{}`".format(key))
                v.append("'{}'".format(value.encode('utf-8')))
            sql = 'INSERT INTO info%s;' %("({}) VALUES ({})".format(",".join(str(r) for r in k),",".join(v)))
            tx.execute(sql);
                # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            # except :
            #     print "SQL write error!"


    def handle_error(self, e):
        print "error:",e