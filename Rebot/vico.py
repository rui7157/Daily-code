#coding:utf-8

import requests
import json
import urllib
import os
import time 
import mp3play
import sys
from robot import Robot
class Speak(object):
    def __init__(self):
        self.key={
             "grant_type":"client_credentials",
             "client_id":"StaCktdGz4qpAMXRHgR6hi2nWV7hUtnK",
             "client_secret":"vuxLXes0u0Dcm9Vv6erdbxsTnYLZcGhk"
        }
        self.filename=os.path.join(os.path.dirname(__file__),"test1.mp3")
    def __call__(self,text="这是测试文本"):
        # access_token=json.loads(requests.post("https://openapi.baidu.com/oauth/2.0/token",data=self.key).content).get("access_token")
        # print access_token
        downloadUrl="http://tsn.baidu.com/text2audio?tex={}&lan=zh&cuid=rui7157&ctp=1&tok={}".format(text.encode('utf-8'),"24.f55b17578d8bd56ded71d36b9d78b4ca.2592000.1475031284.282335-5145581")
        urllib.urlretrieve(downloadUrl,self.filename)
        mp3 = mp3play.load(self.filename)    
        mp3.play()    
        time.sleep(min(30, mp3.seconds())+1)    
        mp3.stop()

if __name__ == '__main__':
    intext=""
    robot=Robot()
    while intext!=u"再见".encode("gbk"):
        intext=raw_input(">>")
        if intext=='q':
            intext=u"再见".encode("gbk")
        answer=robot.moli(intext.decode("gbk"))
        print u"阿呆：{}".format(answer).encode("gbk","ignore")
        Speak()(answer)
    print u"再见！^_^"




