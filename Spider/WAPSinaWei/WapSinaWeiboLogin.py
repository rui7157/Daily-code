#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-16 17:14:48
# @Author  : NvRay (nvray@foxmail.com)

from lxml import etree
import requests
import re
from PIL import Image
import cStringIO
import os
from chardet import detect
import json
import pickle


cok_requests = requests.session()


def write_log(filename="log.txt", mode="wb", text=""):
    with open(os.path.join(os.path.dirname(__file__), filename), mode) as f:
        f.write(text)


class WeiboLogin(object):

     # 记录cookie请求的requests

    def __init__(self):
        # 请输入准备抓取的微博地址
        self.url = "https://weibo.cn"
        self.url_login = 'https://login.weibo.cn/login/'
        self.new_url = self.url

    def get_cookie_request(self):

        if os.path.exists("cookies.cok"):
            cok = open("cookies.cok", "r")
            cookies = pickle.load(cok)
            cok.close()
        else:
            self.login()
            cookies = cok_requests.cookies
            with open("cookies.cok", "w") as cok:
                pickle.dump(cookies, cok)
        cok_requests.cookies.update(cookies)

        return cok_requests

    def login(self):
        html = requests.get(self.url_login).content
        selector = etree.HTML(html)
        password = selector.xpath('//input[@type="password"]/@name')[0]
        vk = selector.xpath('//input[@name="vk"]/@value')[0]
        capid = selector.xpath('//input[@name="capId"]/@value')[0]
        action = selector.xpath('//form[@method="post"]/@action')[0]
        code = self.get_code(html)
        pwd, unm = None, None
        while not all((pwd, unm)):
            pwd = raw_input("username:")
            unm = raw_input("password:")
        self.new_url = self.url_login + action
        data = {'mobile': unm,
                password: pwd,
                'remember': 'on',
                'backURL': 'http://weibo.cn/',
                'backTitle': u'微博',
                'tryCount': '',
                'vk': vk,
                'code': code,
                'capId': capid,
                'submit': u'登录'}
        login_post = cok_requests.post(self.new_url, data=data)  # 登陆post
        write_log(text=login_post.content)
        return login_post

    @staticmethod
    def get_code(html):
        """获取网页验证码
        html验证码content"""
        imgpath = requests.get(re.findall(
            r'<img src="(.*?)" alt="请打开图片显示" />', html)[0]).content
        Image.open(cStringIO.StringIO(imgpath)).show()
        code = raw_input(u"input code:").decode("gbk")
        return code


class Request(WeiboLogin):
    """
    Attribute:Request(callback=None,method="get",headers=None,meta=None)
    callback:callback
    header:web header
    method:request method
    meta:post attr
    """

    def __new__(self, url, callback=None, method="get", headers=None, meta=None):
        WeiboLogin().get_cookie_request()
        self.headers = headers or {}
        self.meta = meta or {}
        if not url:
            return None
        for i in xrange(3):
            response = getattr(cok_requests, method)(url, headers=self.headers)
            if callback:
                if response.status_code == 200:
                    return callback(response=response.content)
            else:
                if response.status_code == 200:
                    return response.content
            if i == 2:
                return None


if __name__ == '__main__':

    WeiboLogin().get_cookie_request()
