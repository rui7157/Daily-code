# -*- coding=utf-8 -*-

import requests
import re
import datetime
import json
import os
from gevent import monkey
monkey.patch_all()
import gevent

TITLE_FILE = os.path.join(os.path.dirname(__file__), "title.txt")
BODY_FILE = os.path.join(os.path.dirname(__file__), "body.txt")


class News(object):
    # 热点新闻采集

    def __init__(self):
        self.article_count = 0  # 保存信息数量
        self.filter_word = [u"习近平"]  # 敏感词

    def write_file(self, title, body):
        for f_word in self.filter_word:
            # 敏感词过滤
            if f_word.encode("gbk") in title or f_word.encode("gbk") in body:
                print u"已经过滤敏感词文章：{}".format(title.decode("gbk"))
                return 0
        with open(TITLE_FILE, "a") as t:
            t.write(title)
        with open(BODY_FILE, "a") as b:
            b.write(body.strip()+"\n")
        self.article_count += 1
        return 1

    def ifeng(self):
        # 凤凰新闻
        count = 0
        url = "http://news.ifeng.com/hotnews/"
        web = requests.get(url, timeout=15).content
        for content in re.findall(r'<td nowrap><h3><a href="(http://news.ifeng.com/a/[0-9]{8}/[0-9]{5,9}_0.shtml)" target="_blank">(.*?)</a></h3></td>', web):
            web_body = requests.get(content[0], timeout=15).content
            try:
                body = re.compile(r"<.*?>").sub("", re.search(
                    r"<!--mainContent begin-->([.\s\S]*?)<!--mainContent end-->", web_body).group(1))  # 提取文章主体并过滤html标签
            except AttributeError, e:
                print u"跳过内容抓取：{}".format(content[1].decode("utf-8")).encode("gbk")
                continue
            if self.write_file(content[1].decode("utf-8").encode("gbk") + "\n", body.decode("utf-8").encode("gbk")):
                count += 1
        print u"成功采集ifeng%s条" % count

    def sina(self, datatype="news_", days=15):
        # 新浪新闻
        count = 0
        for day in range(1, days):
            curren_time = datetime.date.today() + datetime.timedelta(-day)
            url = "http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=qbpdpl&top_time={nowtime}&top_show_num=100&top_order=DESC&js_var={datatype}".format(
                nowtime=curren_time.strftime('%Y%m%d'), datatype=datatype)
            js_retuen_val = requests.get(url, timeout=15).text
            for single_data in json.loads(re.findall("var news_ = (.*?);", js_retuen_val)[0]).get(u"data"):
                # print single_data.get(u"title"), single_data.get(u"url")
                web_body = requests.get(single_data.get(u"url")).content
                print single_data.get(u"title").encode("gbk", "ignore") 
                try:
                    body = re.compile("<.*?>").sub("", re.search(r'id="artibody">([.\s\S]*?)</div>', web_body).group(
                        1)).strip()
                except AttributeError:
                    print u"跳过内容抓取：{}".format(single_data.get(u"title"))
                    continue
                if self.write_file(single_data.get(u"title").encode("gbk", "ignore") + "\n", body.decode("utf-8").encode("gbk")):
                    count += 1
        print u"成功采集sina%s条" % count

    def wy163(self):
        # 网易
        count = 0
        url = "http://news.163.com/rank/"
        web = requests.get(url, timeout=15).content
        for content in re.findall(r'<td class="[a-z]*?"><span>[0-9]*?</span><a href="(.*?)">(.*?)</a></td>', web):
            # print content[1], content[0]
            web_body = requests.get(content[0]).content
            try:
                body = re.compile(r"<.*?>").sub("", re.search(r'<div class="post_text" id="endText">([.\s\S]*?)</div>', web_body).group(
                    1)).replace(u"网易".encode("gbk"), u"本站".encode("gbk"))
            except AttributeError:
                print u"跳过内容抓取：{}".format(content[1].decode("gbk"))
                continue
            if self.write_file(content[1], body):
                count += 1
        print u"成功采集网易%s条" % count

    def sohu(self):
        # 搜狐
        count = 0
        new_types = ["news", "business", "yule", "sports", "fashion", "it"]
        url = "http://pinglun.sohu.com/{new_type}.html"
        for new_type in new_types:
            web = requests.get(url.format(
                new_type=new_type), timeout=15).content
            for content in re.findall(r'<a target="_blank" href="(http://[a-z]{0,16}.sohu.com/[0-9]{8}/n[0-9]{6,13}.shtml)" title="(.*?)">', web):
                web_body = requests.get(content[0]).content
                body = ""
                for p in re.findall(r"<p>(.*?)</p>", web_body):
                    if p:
                        body = body + re.compile(r"<.*?>").sub("", p)
                if self.write_file(content[1].decode("utf-8").encode("gbk", "ignore") + "\n", body):
                    count += 1
        print u"成功采集sohu%s条" % count

    def qq(self):
        # 腾讯新闻
        url = "http://roll.news.qq.com/"

    def mnw(self, page=20):
        # 闽南网
        """china"国内新闻,shehui":社会新闻,world：国际新闻,ent:娱乐新闻,tiyu:体育新闻,cj：财经新闻,digi：数码新闻
        """
        count = 0
        new_types = ["china", "shehui", "world", "ent", "tiyu", "cj", "digi"]
        for new_type in new_types:
            for p in range(1, page):
                if p != 1:
                    url = "http://www.mnw.cn/news/{new_type}/index-{p}.html".format(
                        p=p, new_type=new_type)
                else:
                    url = "http://www.mnw.cn/news/{new_type}/".format(
                        new_type=new_type)
                web = requests.get(url, timeout=15).content
                for content in re.findall(r'<a href="(http://www.mnw.cn/news/%s/[0-9]{1,9}.html)" target="_blank">([^<img].*?)</a>' % new_type, web):
                    web_body = requests.get(content[0]).content
                    try:
                        body = re.compile(r"<.*?>").sub("", re.search(r'<div class="icontent">([.\s\S]*?)</div>', web_body).group(
                            1))
                    except AttributeError:
                        print u"跳过内容抓取：{}".format(content[1].decode("utf-8"))
                        continue
                    if self.write_file(content[1].decode("utf-8").encode("gbk", "ignore") + "\n", body.decode("utf-8").encode("gbk", "ignore")):
                        count += 1
        print u"成功采集闽南网%s条" % count

    def cicnn(self, page=20):
        # 江汛网
        count = 0
        new_types = {"mil": "30", "world": "29", "wonders": "139"}
        for new_type, new_type_number in new_types.items():
            for p in range(1, page):
                if p != 1:
                    url = "http://www.cicnn.com/news/mil/list-{new_type_number}-{p}.html".format(
                        p=p, new_type=new_type, new_type_number=new_type_number)
                else:
                    url = "http://www.cicnn.com/news/{new_type}/".format(
                        new_type=new_type)
                web = requests.get(url, timeout=30).content
                for content in re.findall(r'<a target="_blank" href="(http://www.cicnn.com/news/%s/[0-9]{1,9}.html)">(.*?)</a>' % new_type, web):
                    web_body = requests.get(content[0]).content
                    body = re.compile(
                        r"<.*?>").sub("", re.search(r'<div id="content">([.\s\S]*?)</div>', web_body).group(1)).replace(u"江汛网".encode("gbk"),u"本站".encode("gbk"))
                    if self.write_file(content[1] + "\n", body):
                        count += 1
        print u"成功采集cicnn%s条" % count

    def chinanews(self, page=10):
        # 中国新闻网  (滚动新闻最大10页)
        count = 0
        url = "http://www.chinanews.com/scroll-news/news{p}.html"
        for p in range(1, page):
            web = requests.get(url.format(p=p), timeout=30).content
            for content in re.findall(r'<div class="dd_bt"><a href="(http://www.chinanews.com/[a-z|/]*/[0-9]{4}/\w{2}-\w{2}/[a-z0-9]+.shtml)">(.*?)</a></div><div class="dd_time">', web):
                # print content[1], content[0]
                print content[0]
                web_body = requests.get(content[0]).content
                print web_body
                try:
                    body = re.compile(r"<script.*?>.*?</script>|<.*?>").sub("", re.search(
                        r'<!--\u6b63\u6587start-->([.\s\S]*?)<!--\u6b63\u6587start-->', web_body).group(1))
                except AttributeError:
                    print u"跳过内容抓取：{}".format(content[1].decode("gbk"))
                    continue
                if self.write_file(content[1] + "\n", body):
                    count += 1
        print u"成功采集chinanews %s条" % count


if __name__ == "__main__":
    news = News()
    # news.chinanews()
    p = gevent.spawn
    gevent.joinall([gevent.spawn(news.ifeng), gevent.spawn(news.sina), gevent.spawn(
        news.wy163), gevent.spawn(news.mnw, 300), p(news.cicnn, 300), p(news.sohu)])#, p(news.chinanews)
    print u"采集完毕"
#pyinstaller.py -F -p D:\tmp\tmp_dev_root\python\tutorial_summary\make_exe\BlogsToWordpress\libs;D:\tmp\tmp_dev_root\python\tutorial_summary\make_exe\BlogsToWordpress\libs\crifan;D:\tmp\tmp_dev_root\python\tutorial_summary\make_exe\BlogsToWordpress\libs\crifan\blogModules;D:\tmp\tmp_dev_root\python\tutorial_summary\make_exe\BlogsToWordpress\libs\thirdparty;D:\tmp\tmp_dev_root\python\tutorial_summary\make_exe\BlogsToWordpress\libs\thirdparty\chardet; ..\BlogsToWordpress\BlogsToWordpress.py