#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/4 9:42
# Change Activity:
#                   2018/4/4
# @Author  : NvRay
# @File    : logForWeb.py
# @Software: PyCharm

import logging
import functools
import webbrowser
import os
from aiohttp import web
import asyncio
import websockets
from multiprocessing import Process,Queue
from jinja2 import Environment
from jinja2 import FileSystemLoader
import platform
import socket
import struct


"""
日志调试web平台
"""


logging.basicConfig(level=logging.INFO)

if not "logp" in locals():
    logp = print

sysType = platform.system()
if sysType == "Linux":
    import fcntl
DEBUG = True
KNXOBJ = dict()
coroutines = None

def getIpAddress(ifname):
    # 获取IP地址
    if sysType == "Linux":
        if isinstance(ifname, str):
            ifname = ifname.encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        myaddr = socket.inet_ntoa(
            fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])  # SIOCGIFADDR
    elif sysType == "Windows":
        # 获取本机电脑名
        myname = socket.getfqdn(socket.gethostname())
        # 获取本机ip
        myaddr = socket.gethostbyname(myname)
    else:
        logp("Error Unknown platform!")
        return ""

    return myaddr

#绑定路由和函数
class RequestRoute(object):

    def __init__(self,app,fn,path):
        for a in list(locals().keys()):
            setattr(self, a, locals()[a])

    def __call__(self, *args, **kwargs):
        pass

def route(path,*method):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kargs):
            return web.Response(body=func(*args,**kargs),content_type='text/html',charset='utf-8')
        wrapper._path = path
        if len(method)>0:
            wrapper._method = method[0].upper()
        else:
            wrapper._method = "GET"
        return wrapper
    return decorator


class RecvLogMsg(Process):
    def __init__(self,recvQueue):
        self.recvQueue = recvQueue
        super(RecvLogMsg,self).__init__()

    def run(self):
        print("start recv log listen Process")
        port = 9999
        localIP = getIpAddress("eth0")

        recvQueue = self.recvQueue
        loop = asyncio.get_event_loop()
        class ListenUDPunicast:
            def connection_made(self, transport):
                self.transport = transport

            def error_received(self):
                logging.warning("log received error!")

            def datagram_received(self, data, addr):
                self.fromAddr = addr
                print(data)
                recvQueue.put((addr,data))

        listen = loop.create_datagram_endpoint(ListenUDPunicast, local_addr=(localIP, port))
        loop.run_until_complete(listen)
        loop.run_forever()


class SendLogMsg(Process):
    def __init__(self,q):
        self.q = q
        super(SendLogMsg,self).__init__()

    def run(self):
        print("start webSocket send Process")
        async def echo(websocket, path):
            while 1:
                if not self.q.empty():
                    res = self.q.get()
                    sendData = "{}>>{}".format(res[0][0],res[1].decode())
                    print("send data :",sendData)
                    await websocket.send(sendData)

        asyncio.get_event_loop().run_until_complete(
            websockets.serve(echo, '127.0.0.1', 9998))
        asyncio.get_event_loop().run_forever()



#视图函数

@route("/")
def index(request):
    return request.app["template"].get_template('index.html').render()

@route("/test")
def test(request):
    return "Test Info "

@route("/watchdebug")
def watchdebug(request):
    #网页滚动日志
    """
    websocket 实时更新调试信息
    """
    return "debug"


class Route(object):
    """
    搜索全局路由函数注册
    """
    def __init__(self,app):
        self.app = app
        self.allRouteFunc = []
        self.routeMap = dict()
        self.__route()

    def __addRoute(self,func):
        method = func._method
        path = func._path
        self.routeMap[path] = "{}:{}".format(method,func.__name__)
        print(method,path,func)
        self.app.router.add_route(method, path, func)

    def __route(self):
        for fName in globals():
            if getattr(globals()[fName], "_method", None) and getattr(globals()[fName], "_path", None):
                rFunc = globals()[fName]
                self.allRouteFunc.append(rFunc)
                self.__addRoute( rFunc)

    def map(self):
        return self.routeMap

    def __repr__(self):
        res = ""
        for k,v in self.routeMap.items():
            res +="'{}' => {}\n".format(k,v)
        return res



async def init(loop,addr):
    ip,port = addr
    app = web.Application(loop=loop)
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "template"), 'utf-8'))
    app["template"] = env
    Route(app)
    srv = await loop.create_server(app.make_handler(), ip, port)
    webbrowser.open("http://127.0.0.1:5001")
    logging.info('server started at http://127.0.0.1:5001...')
    return srv

def run(ip="0.0.0.0",port=5001):
    recvQueue = Queue()
    # 日志消息监听 存入队列消息
    recvT = RecvLogMsg(recvQueue)
    #开启websocket 日志推送 取出队列消息
    sendT = SendLogMsg(recvQueue)
    recvT.start()
    sendT.start()
    addr = (ip,port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop,addr))
    loop.run_forever()


if __name__ == "__main__":
    run()

