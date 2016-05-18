#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-17 09:45:10
# @Author  : Your Name (nvray@foxmail.com)
# @Link    : 
# @Version : $Id$

import os
import sys, urllib, urllib2, json


def speak(content):

    req = urllib2.Request('http://i.itpk.cn/api.php?question=123&api_key=dad63f4a51af1f3ca78a1af6247a5a74&api_secret=llkg9pol12ib&question={info}&limit=8'.format(info=urllib.quote(content)))

    req.add_header("apikey", "c92bd543d8b5391c861d1a19e59c6cdf")

    resp = urllib2.urlopen(req)
    content = resp.read()
    if(content):
        print content.decode("utf-8").encode("gbk")

if __name__=="__main__":
    print "-"*20
    print u"机器人已经启动...."
    print u"输入“quit”结束程序."
    print "-"*20
    while 1:
        content=raw_input(">>")
        if content=="quit":
            exit()
        speak(content.decode("gbk").encode("utf-8"))

