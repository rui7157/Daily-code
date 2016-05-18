# -*- coding: utf-8 -*-
import sys
import urllib
import urllib2
import json
import os

txt_file = os.path.join(os.path.dirname(__file__), "url.txt")


def req(page):
    req = urllib2.Request(
        'http://apis.baidu.com/txapi/social/social?num=50&page=%s' % page)
    req.add_header("apikey", "c92bd543d8b5391c861d1a19e59c6cdf")
    resp = urllib2.urlopen(req)
    content = resp.read()
    if(content):
        js = json.loads(content)
        for url in js.values()[2]:
            with open(txt_file, "a") as f:
                f.write(url.get("url").join('\n'))
                print url.get("url")


if __name__ == "__main__":
    page = raw_input(u"请输入获取页数：".encode("gbk"))
    try:
        for i in range(1, int(page)):
            req(i)
    except:
        print u"输入数据有误！"
