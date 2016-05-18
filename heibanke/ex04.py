#!coding:utf-8
import pytesseract
import requests
import re
import os
from PIL import Image
import cStringIO
def captcha_img(img):
    img_path=cStringIO.StringIO(img)
    png=Image.open(img_path)
    png.show()
    return pytesseract.image_to_string(png,lang='eng')

def openurl(pwd):
    cookies=dict(   
        csrftoken="bRx2wea3i1wXbEJAz27ESH8Gvs4tYgti", sessionid="qkwknpbcp0ajh4fvnukbn00w7s485xtk")

    getweb=requests.get("http://www.heibanke.com/lesson/crawler_ex04/",cookies=cookies).content
    r_captcha=re.compile(r'<img src="/captcha/image/(.*?)/" ')
    captcha_0=re.findall(r_captcha,getweb)[0]
    url="http://www.heibanke.com/captcha/image/{}/".format(captcha_0)
    # print url
    print url
    img=requests.get(url,stream=True).content

    captcha_num=captcha_img(img)
    data=dict(csrfmiddlewaretoken="bRx2wea3i1wXbEJAz27ESH8Gvs4tYgti",username="nvray")
    data["captcha_0"]=captcha_0
    data["captcha_1"]=captcha_num
    web_data=requests.post("http://www.heibanke.com/lesson/crawler_ex02/",data=data,cookies=cookies).content
    # print web_data.find("密码错误")
    if web_data.find("密码错误")!=-1:
        print "错误:{pwd}".format(pwd=pwd)
    elif web_data.findall("验证码输入错误")!=-1:
        print "验证码错误"
        openurl(pwd)
    else:
        print "账号：nvray\n密码:{pwd}".format(pwd=pwd)
        return "账号：nvray\n密码:{pwd}".format(pwd=pwd)
    return openurl(pwd+1)  

if __name__=="__main__":
    openurl(0)