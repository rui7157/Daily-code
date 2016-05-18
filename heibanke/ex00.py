#coding:utf-8

import requests
import re

def openurl(key):
    webdata=requests.get("http://www.heibanke.com/lesson/crawler_ex00/{key}".format(key=key)).content
    r_num=re.compile(r"<h3>.*?(\d+).*<")
    resulth=re.findall(r_num, webdata)
    print "num:",resulth[0]
    return openurl(resulth[0])
    
    

if __name__ =="__main__":
    openurl("")