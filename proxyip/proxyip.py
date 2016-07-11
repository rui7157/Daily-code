#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-17 17:29:31
# @Author  : NvRay (nvray@foxmail.com)

import requests
import re
import os
from gevent import monkey
monkey.patch_socket()
import gevent

address = {
    "国内高匿": "nn",
    "国内高透": "nt",
    "国外高匿": "wn",
    "国外高透": "wt"
}
save_file = os.path.join(os.path.dirname(__file__), "proxyip.txt")

requests = requests.session()


class Proxy(object):
    def __init__(self, page, addr):
        self.page = page
        self.data = list()
        self.addr = address.get(addr)

    def web(self, page):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
            "Host": "www.xicidaili.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate"
        }
        if page == 0:
            web = requests.get("http://www.xicidaili.com/nt",
                               headers=headers,proxies={"HTTP":"101.21.100.106:8888"}).text
        else:
            web = requests.get("http://www.xicidaili.com/{addr}/{page}".format(
                page=page, addr=self.addr), headers=headers).text
        data = re.findall(
            r'<tr class="odd">[\s\S]*?<td>(.*?)</td>[\s\S]*?<td>(.*?)</td>[\s\S]*?">(.*?)</a>', web)
        for info in data:
            self.data.append({
                "ip": info[0],
                "port": info[1],
                "addr": info[2]
            })

    def run(self):
        gevent.joinall([gevent.spawn(self.web, p) for p in range(self.page)])
        return self.data

if __name__ == '__main__':
    ip = Proxy(300, "国内高匿").run()

    ipdata=dict()
    for i in ip:
        with open(save_file, "a") as f:
            f.write(u"{ip} {port} {addr}\n".format(ip=i.get("ip"),
                                                   port=i.get("port"), addr=i.get("addr")).encode("utf-8"))

        print u"ip:%s port:%s addr:%s" % (i.get("ip"), i.get("port"), i.get("addr"))
