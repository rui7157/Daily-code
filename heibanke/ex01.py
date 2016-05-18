#!coding:utf-8
import requests
import gevent
#fIq7uPCWImQeKpj4CwQp3VBUca92juGM
#fIq7uPCWImQeKpj4CwQp3VBUca92juGM

def openurl(pwd):
    data={
        "csrfmiddlewaretoken": "fIq7uPCWImQeKpj4CwQp3VBUca92juGM",
        "username":"nvray"}
    data["password"]=str(pwd)
    web_data=requests.post("http://www.heibanke.com/lesson/crawler_ex01/",data=data).content
    # print web_data.find("密码错误")
    if web_data.find("密码错误")!=-1:
        print "错误:{pwd}".format(pwd=pwd)
    else:
        print "账号：nvray\n密码:{pwd}".format(pwd=pwd)
        return "账号：nvray\n密码:{pwd}".format(pwd=pwd)
    return openurl(pwd+1)    

if __name__=="__main__":
    openurl(0)