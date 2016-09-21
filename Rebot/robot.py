#coding:utf-8
#key:    dad63f4a51af1f3ca78a1af6247a5a74 
#secret: llkg9pol12ib
import requests
import json
class Robot(object):
    def moli(self,text="你好"):
        """return data type ： unicode"""
        return requests.get("http://i.itpk.cn/api.php?question={}&api_key={}&api_secret={}".format(text.encode("utf-8"),"dad63f4a51af1f3ca78a1af6247a5a74","llkg9pol12ib")).text
    def tuling(self,text="你好"):
        data={
            "key":"9ce9e5f76ff64f53a0f1e09df91bccc9",
            "info":text
        }
        return json.loads(requests.post("http://www.tuling123.com/openapi/api",data=data).content).get("text")