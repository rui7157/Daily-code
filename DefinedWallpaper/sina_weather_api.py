#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-14 19:06:21
# @Author  : NvRay (you@example.org)


import urllib,urllib2
import json
from setWarpaper import NoteWallpaper



class weather_api(object):
    """
    新浪天气查询接口
    city:城市  
    day:天数 (0：当天)
    """

    def __init__(self,city):
        self.city=city
        # self.city=city

    def query(self):
        url = 'http://apis.baidu.com/heweather/weather/free?city=beijing'   
        req = urllib2.Request("http://apis.baidu.com/heweather/weather/free?city={city}".format(city=self.city))

        req.add_header("apikey", "c92bd543d8b5391c861d1a19e59c6cdf")

        resp = urllib2.urlopen(req)                                                    
        # f=urllib2.urlopen(req)
        weather_data=resp.read()
        return json.loads(weather_data)        # print data
#c92bd543d8b5391c861d1a19e59c6cdf
if __name__ == "__main__":
    data=weather_api(u"chengdu".encode("gbk")).query()["HeWeather data service 3.0"][0]
    
    # print u"天气:%s" %data["now"]["cond"]["txt"]
    # print u"温度 {} ℃ ".format(data["now"]["tmp"])
    # print u"{dir} {sc}级 风速{spd}kmph".format(dir=data["now"]["wind"]["dir"],sc=data["now"]["wind"]["sc"],spd=data["now"]["wind"]["spd"])
    # print u"温馨提示:{txt}".format(txt=data["suggestion"]["comf"]["txt"])
    # print u"更新:{}".format(data["basic"]["update"]["loc"])
    txt=data["suggestion"]["comf"]["txt"]
    txt="\n".join(txt[i:i+15] for i in xrange(0,len(txt),15))
    text=u"""
城市:{city}
天气:{cond}
温度:{tmp} ℃ 
{dir} {sc}级 风速{spd}kmph
温馨提示:
{txt}
更新:{update}
    """.format(city=data["basic"]["city"],cond=data["now"]["cond"]["txt"],tmp=data["now"]["tmp"],dir=data["now"]["wind"]["dir"],sc=data["now"]["wind"]["sc"],spd=data["now"]["wind"]["spd"],txt=txt,update=data["basic"]["update"]["loc"])
    print text
    if NoteWallpaper(text,imgpath="C:\\wallpaper\\book.bmp").setWallpaper(verticalspacing=30,leftmargin=500)=="FilePathError":
        print u"壁纸路径错误设置失败"
