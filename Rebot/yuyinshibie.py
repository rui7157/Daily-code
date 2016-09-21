#coding:utf-8

import requests
import json
import urllib
import os
import time 
import sys
import base64
class Listen(object):


    def __init__(self):
        self.key={
             "grant_type":"client_credentials",
             "client_id":"StaCktdGz4qpAMXRHgR6hi2nWV7hUtnK",
             "client_secret":"vuxLXes0u0Dcm9Vv6erdbxsTnYLZcGhk"
        }
        self.filename=os.path.join(os.path.dirname(__file__),"test1.mp3")
    def __call__(self):
        access_token=json.loads(requests.post("https://openapi.baidu.com/oauth/2.0/token",data=self.key).content).get("access_token")
        
        c=open("c.txt","a+")
        with open("test1.mp3","rb") as f:
            base64.encode(f,c)  
        vdata=c.read()
        c.close()
        data={
            "format":"wav",
            "rate":8000,
            "channel":1,
            "token":access_token.encode('utf-8'),
            "cuid":"rui7157",
            "len":4096,
            "speech":vdata,
        }
        print data
        result=requests.post("http://vop.baidu.com/server_api",data=data).content
        print result

if __name__ == '__main__':
    Listen()()



