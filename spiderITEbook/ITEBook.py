    #coding:utf-8
import requests
import re
import urllib
import pymongo
"""
爬取电子书下载地址，存入MonogoDB
"""


class Ebook(object):
    webUrl="http://www.allitebooks.com/"
    reIndexUrl=r'<a href="http://www.allitebooks.com/([\w|-]*?)/">'
    pageUrl="http://www.allitebooks.com/programming/page/{}/"
    reBookUrl=r'<h2 class="entry-title"><a href="(.*?)" rel="bookmark">.*?</h2>'
    reBookDownload=r"http://file.allitebooks.com/.*?\.pdf"

    def __init__(self):
        self.bookDownloadUrl=list()

    def index(self):
        indexContent=requests.get(self.webUrl).content
        proUrl=re.findall(self.reIndexUrl,indexContent)
        return proUrl

    def pageContent(self):
        preTypeUrl=self.index()
        for bType in preTypeUrl:
            bookType=self.webUrl+bType
            pageNum=1
            singlePageContent=""
            while not "No Posts Found" in singlePageContent:
                singlePageContent=requests.get(self.pageUrl.format(pageNum)).content #每页内容
                prePageUrl=re.findall(self.reBookUrl,singlePageContent) 
                for url in prePageUrl:
                    book=requests.get(url).content #一本书的内容页
                    downloadUrl=re.search(r"http://file\.allitebooks\.com/.*?\.pdf",book)
                    if downloadUrl:
                        print "{'%s':'%s'}" %(bType,downloadUrl.group(0))
                        self.insertData({bType:downloadUrl.group(0)})
                        print downloadUrl.group(0)
                pageNum+=1

    def insertData(self,data):
        client = pymongo.MongoClient('localhost', 27017)
        db=client.ebook #数据库
        book=db.book   #表
        book.insert(data)
if __name__ == '__main__':
    Ebook().pageContent()