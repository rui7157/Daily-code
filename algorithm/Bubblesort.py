#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-15 10:57:06
# @Author  : NvRay (nvray@foxmail.com)
# 冒泡排序算法


import sys
import time
sys.setrecursionlimit(9999999) #递归深度

import generate_number





def Bluble(data):
    count=len(data)
    for n in range(count):
        for m in range(n+1,count):
            if data[n]>data[m]:
                data[n],data[m]=data[m],data[n]
    return data  

if __name__=="__main__":
    starttime=time.time()
    data=generate_number.rend(10000)#生成数据
    print Bluble(data)
    print "计算一共用时：%ss" %(time.time()-starttime)