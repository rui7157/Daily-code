#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/11 10:49
# Change Activity:
#                   2018/4/11
# @Author  : NvRay
# @File    : linuxTestPro.py
# @Software: PyCharm

from socket import *
webLogServer ={
    "ip":"192.168.0.30",
    "port":9999
}
def logp(msg):
    msg = msg.encode()
    skt = socket(AF_INET,SOCK_DGRAM)
    skt.sendto(msg,(webLogServer["ip"],webLogServer["port"]))
    skt.close()

from time import sleep
import datetime

a = 0
while 1:
    sleep(1)
    a+=1
    logp("<{t} - {n}> 来自服务器第{n}声问候~".format(t = datetime.datetime.now(),n =a))