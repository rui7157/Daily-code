# coding:utf-8
import requests
import re
import os
import time
from threading import Thread
from gevent import monkey
monkey.patch_socket()
import gevent


class Query():

    def __init__(self, key, url):
        if all([isinstance(key, list), isinstance(url, list)]):
            self.key = key
            self.url = url
        else:
            raise ValueError
        self.result = dict()

    def __request(self, key, rn=50):
        baidu_single_page = requests.get(
            "http://www.baidu.com/s?wd={key}&rn={rn}".format(key=key, rn=rn))
        baiduurl_class_div = re.findall(
            r'<div class="f13">(.*?)</div>', baidu_single_page.text)
        if baiduurl_class_div:
            for url in self.url:
                for index, d in enumerate(baiduurl_class_div):
                    if url.replace("\n", "") in d:
                        print url, index
                        self.result[key] = [url, index + 1]

    def start(self,concurrent=False):
        if not concurrent:
            for key in self.key:
                self.__request(key)
        else:
            gevent.joinall(
                [gevent.spawn(self.__request, key.replace("\n", "")) for key in self.key])
        return self.result


if __name__ == "__main__":
    k = open(os.path.join(os.path.dirname(__file__), "key.txt")).readlines()
    u = open(os.path.join(os.path.dirname(__file__), "host.txt")).readlines()
    st_time = time.time()
    data = Query(k, u).start()
    dirpath = os.path.dirname(__file__)
    with open(os.path.join(str(dirpath), "BaiduQuery.txt"), "w") as f:
        for key, url_rank in data.items():
            wrt_data = "{key} {url} {rank} \n".format(
                key=key, url=url_rank[0], rank=url_rank[1])
            f.write(wrt_data)
    print u"查询完成，文件保存在{path}.".format(path=os.path.join(str(dirpath), "BaiduQuery.txt"))
    print u"耗时%fs" % (time.time() - st_time)
    raw_input(u"按任意键退出……".encode("gbk"))
