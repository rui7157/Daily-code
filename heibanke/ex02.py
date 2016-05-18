#!coding:utf-8
import requests
import gevent
#fIq7uPCWImQeKpj4CwQp3VBUca92juGM
#cookies:sessionid=qkwknpbcp0ajh4fvnukbn00w7s485xtk

def openurl(pwd):
    data={
        "csrfmiddlewaretoken": "bRx2wea3i1wXbEJAz27ESH8Gvs4tYgti",
        "username":"nvray"}
    cookies={
    "sessionid":"qkwknpbcp0ajh4fvnukbn00w7s485xtk",
    "csrftoken":"bRx2wea3i1wXbEJAz27ESH8Gvs4tYgti"
    }    
    data["password"]=str(pwd)
    web_data=requests.post("http://www.heibanke.com/lesson/crawler_ex02/",data=data,cookies=cookies).content
    # print web_data.find("密码错误")
    if web_data.find("密码错误")!=-1:
        print "错误:{pwd}".format(pwd=pwd)
    else:
        print "账号：nvray\n密码:{pwd}".format(pwd=pwd)
        return "账号：nvray\n密码:{pwd}".format(pwd=pwd)
    return openurl(pwd+1)    

if __name__=="__main__":
    openurl(0)