# coding:utf-8

import requests
import re
from gevent import monkey
monkey.patch_socket()
import gevent
class Tieba(object):
    def __init__(self, url):
        self.url = url

    def start(self, page):
        content = requests.get(self.url % page).text
        titles = re.findall(
            r'<a href="(.*?)" title="(.*?)" target="_blank" class="j_th_tit ">', content)
        for index, title in enumerate(titles):
            print "%s.%s %s" % (index, title[1], "http://tieba.baidu.com" + title[0])

if __name__ == '__main__':
    url = "http://tieba.baidu.com/f?kw=python3&pn=%s"
    page_num = raw_input("Please enter the number of pages:")
    t = Tieba(url)
    if page_num.isdigit():
        gevent.joinall([gevent.spawn(t.start,page*50) for page in range(int(page_num))]) 
    else:
        print "please enter a number!"