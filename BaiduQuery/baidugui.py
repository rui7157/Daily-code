#!coding:utf-8
from PyQt4 import QtCore, QtGui
import sys,os
import threading
import requests
import re
import os
import time
from gevent import monkey
monkey.patch_socket()
import gevent
 
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
from functools import partial

class ArgsError(Exception):
    pass

class Query(object):

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

class BaiduQuery(threading.Thread):
    def __init__(self,frame):
        threading.Thread.__init__(self)
        self.frame=frame
    def run(self): 
        self.frame.okbutton.setText(u"正在查询…")
        self.frame.okbutton.setCheckable(False)
        try:
            self.key=open(self.frame.filetext.text()).readlines()
            self.url=open(self.frame.filetext2.text()).readlines()
        except IOError,e:
            self.frame.errorpath()
            return None
        if all((self.key,self.url)):
            data=Query(self.key,self.url).start(True)     
            dirpath=QtGui.QFileDialog.getExistingDirectory(self.frame,u"保存路径",os.path.dirname(sys.argv[0]))
            with open(os.path.join(str(dirpath),"BaiduQuery.txt"),"w") as f:
                for key,url_rank in data.items():
                    wrt_data="{key} {url} {rank} \n".format(key=key,url=url_rank[0],rank=url_rank[1])
                    f.write(wrt_data)
            QtGui.QMessageBox.information(self.frame,u"提醒",u"保存成功！")      
        else:
            self.frame.nofile()
        self.frame.okbutton.setText(u"查询")
class Ui_MainWindows(QtGui.QWidget):
    def __init__(self):
        self.key=""
        self.url=""

        QtGui.QWidget.__init__(self)    
        self.setWindowTitle(u"百度排名查询工具")

        self.filetext = QtGui.QLineEdit(os.path.join(os.path.dirname(sys.argv[0]),"key.txt"))
        inputfile=QtGui.QPushButton(u"选择文件")
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(u"关键字:"))
        hbox.addWidget(self.filetext)       
        hbox.addWidget(inputfile)

        self.filetext2 = QtGui.QLineEdit(os.path.join(os.path.dirname(sys.argv[0]),"host.txt"))
        inputfile2=QtGui.QPushButton(u"选择文件")
        hbox2= QtGui.QHBoxLayout()
        hbox2.addWidget(QtGui.QLabel(u"网  址:"))
        hbox2.addWidget(self.filetext2)     
        hbox2.addWidget(inputfile2)

        self.okbutton=QtGui.QPushButton(u"查询")
        self.okbutton.setCheckable(True)
        hbox3=QtGui.QHBoxLayout()
        hbox3.addStretch()
        hbox3.addWidget(self.okbutton)
        hbox3.addStretch()

        vbox=QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        self.setLayout(vbox)
        self.clicked=partial(self.openfile_clicked,filetype="key")
        self.connect(inputfile,QtCore.SIGNAL("clicked()"),self.clicked)
        self.clicked=partial(self.openfile_clicked,filetype="url")
        self.connect(inputfile2,QtCore.SIGNAL("clicked()"),self.clicked)
        self.connect(self.okbutton,QtCore.SIGNAL("clicked()"),self.query)
        self.resize(400, 100)

    def openfile_clicked(self,filetype):
        filename=QtGui.QFileDialog.getOpenFileName(self,'Open file', os.path.dirname(sys.argv[0]),"Text Files (*.txt);;All Files (*)")
        if filename:
            if filetype=="key":
                self.filetext.setText(filename)
                self.key=open(filename).readlines()
            elif filetype=="url":
                self.filetext2.setText(filename)
                self.url =open(filename).readlines()
            else:
                raise ArgsError 

    def nofile(self):
        QtGui.QMessageBox.critical(self,u"警告",u"未选择文件!")  

    def errorpath(self):
        QtGui.QMessageBox.critical(self,u"警告",u"错误的文件或路径!")  

    def query(self):
        if self.okbutton.isCheckable():
            BaiduQuery(self).start()


        
app=QtGui.QApplication(sys.argv)
w=Ui_MainWindows()
# w.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
w.setWindowFlags(w.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint) #禁用最大化按钮
w.show()
sys.exit(app.exec_())