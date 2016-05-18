#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-16 09:51:21
# @Author  : Your Name (nvray@foxmail.com)
# @Link    :
# @Version : $Id$

import time
import urllib2
import urllib
import base64
import json
import re
import os
import binascii
import Cookie
import cookielib


class LoginWeibo(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, login_url="http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"):
        j_data = self.get_sso()
        postdata = {
            'entry': "weibo",
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            'pagerefer': "",
            'vsnf': '1',
            'su': self.get_user(),
            'service': 'miniblog',
            'servertime': j_data.get("servertime"),
            'nonce': j_data.get("nonce"),
            'pwencode': 'rsa2',
            'rsakv': j_data.get("rsakv"),
            'sp': self.get_passwd(j_data.get("pubkey"), j_data.get("servertime"), j_data.get("nonce")),
            'sr': "1440*900",
            'encoding': 'UTF-8',
            'prelt': '503',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }

        cookie = cookielib.MozillaCookieJar("Cookie.txt")
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

        result = opener.open(login_url, urllib.urlencode(postdata))

        cookie.save(ignore_discard=True, ignore_expires=True)

        html = opener.open(
            "http://weibo.com/p/1005055887581312").read()
        with open(os.path.join(os.path.dirname(__file__), "text.html"), "wb") as f:
            f.write(html)
        print "执行完毕"

    def get_sso(self):
        prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSO`Controller.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=%s' % (
            base64.b64encode(self.username), int(time.time()*1000))
        sso_data = urllib2.urlopen(prelogin_url).read()

        # sso_data = re.findall(r"sinaSSOController\.preloginCallBack\((.*?)\)", sso_data)[0]
        if sso_data:
            return json.loads(sso_data)
        else:
            raise TypeError

    def get_user(self):
        return base64.b64encode(self.username)

    def get_passwd(self, pubkey, servertime, nonce):
        import rsa
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + \
            str(self.password)  # 拼接明文js加密文件中得到
        passwd = rsa.encrypt(message, key)  # 加密
        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。

        return passwd


if __name__ == "__main__":
    LoginWeibo("18771994057", "13733431563").login()
