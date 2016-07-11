#coding:utf-8 
from PyQt4 import QtCore, QtGui
import qdarkstyle
import sys
import requests
import re
import os
import time
import xlwt
import datetime
from threading import Thread
from gevent import monkey
monkey.patch_socket()
monkey.patch_ssl()
import gevent

reload(sys)
sys.setdefaultencoding("utf-8")
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
print u"软件已经启动......"

def generate_xls(urls, keys, result,filename):
    """保存数据到excel文件"""
    xls_file = xlwt.Workbook()
    sheet = xls_file.add_sheet(unicode(filename), cell_overwrite_ok=True)
    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.colour_index = 2
    font0.bold = True
    style0 = xlwt.XFStyle()
    style0.font = font0
    row = 0
    sheet.col(0).width = 256 * 20
    sheet.col(1).width = 256 * 30
    sheet.col(2).width = 256 * 20

    sheet.write(0, 0, u"网址", style0)
    sheet.write(0, 1, u"关键词", style0)
    sheet.write(0, 2, u"排名", style0)
    if urls != None and keys != None and result != None:
        for url, key, res in zip(urls, keys, result):
            row += 1
            sheet.write(row, 0, url.decode("utf-8"))
            sheet.write(row, 1, key.decode("utf-8"))
            sheet.write(row, 2, res.decode("utf-8"))
    fpath=os.path.join(os.path.dirname(sys.argv[0]),u"{}.xls".format(unicode(filename))) #保存文件路径
    print u"[提示]：文件已保存到{}".format(fpath)
    xls_file.save(fpath)

class Query(Thread):
    result = list()
    def __init__(self, key, url,Qobj):
        Thread.__init__(self)
        if all([isinstance(key, list), isinstance(url, list)]):
            self.key = key
            self.url = url
        else:
            raise ValueError
        self.Qobj=Qobj
        self.count=0
    def __request(self, key,se, rn=5):
        for pn in xrange(0,rn):
            try:
                if se=="baidu":
                    #百度搜索
                    print u"百度:{}".format(key)
                    baidu_single_page = requests.get(
                        "http://www.baidu.com/s?wd={key}&pn={pn}".format(key=key, pn=pn*10),timeout=15)
                    baiduurl_class_div = re.findall(
                        r'class="c-showurl"(.*?)</a>', baidu_single_page.text)
                    
                elif se=="qihu":
                    #360搜索
                    print u"360搜索:{}".format(key)
                    baidu_single_page = requests.get(
                        "https://www.so.com/s?q={key}&pn={pn}".format(key=key, pn=pn+1),timeout=15)
                    baiduurl_class_div = re.findall(
                        r'<cite>(.*?)</cite>', baidu_single_page.text)
                    
                elif se=="sousou":
                    #搜狗
                    print u"搜狗:{}".format(key)
                    baidu_single_page = requests.get(
                        "https://www.sogou.com/web?query={key}&page={pn}".format(key=key, pn=pn+1),timeout=15)
                    baiduurl_class_div = re.findall(
                        r'<cite id="cacheresult_info([\s\S]*?)</cite>', baidu_single_page.text)

                elif se=="shenma":
                    #神马搜索
                    print u"神马:{}".format(key)
                    header={"User-Agent":"Nokia6600/1.0 (4.03.24) SymbianOS/6.1 Series60/2.0 Profile/MIDP-2.0 Configuration/CLDC-1.0"} #神马移动端搜索，模拟塞班手机
                    baidu_single_page = requests.get(
                        "http://m.sm.cn/s?q={key}&page={pn}".format(key=key, pn=pn+1),headers=header,timeout=15)
                    baiduurl_class_div = re.findall(
                        r'<div class="other">(.*?)</div></div>', baidu_single_page.text)
            except requests.models.ConnectionError:
                print u"关键词:{}，第{}页，页面请求超时已经跳过!".format(key,str(pn+1)) #处理请求超时
            if baiduurl_class_div:
                for url in self.url:
                    for index, d in enumerate(baiduurl_class_div):
                        if url.replace("\n", "") in d:
                            self.Qobj.tableView.setRowCount(self.count+1) #动态添加表格数据
                            self.Qobj.tableView.setItem(self.count,0,QtGui.QTableWidgetItem(unicode(key))) #加入表格
                            self.Qobj.tableView.setItem(self.count,1,QtGui.QTableWidgetItem(unicode(url)))
                            self.Qobj.tableView.setItem(self.count,2,QtGui.QTableWidgetItem(u"第{}页第{}个".format(str(pn+1),str(index + 1))))
                            Query.result.append([url, pn+1,index + 1,key])  #保存数据
                            self.count+=1 #记录结果数量


    def run(self):
        if self.Qobj.se == "qihu":
            #360搜索快速会封IP，因此关闭异步高速请求
            print u"360搜索防屏蔽开始慢速模式，请耐心等待..."
            for key in self.key:
                self.__request(key,"qihu")
                time.sleep(3) #加入搜索延时
        else:
            #异步
            gevent.joinall([gevent.spawn(self.__request, key,self.Qobj.se) for key in self.key])
        print "*"*20
        print u"本次搜索完毕"
        print "*"*20



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(900,700)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.baidu=QtGui.QRadioButton(Form)
        self.baidu.setObjectName(_fromUtf8("baidu"))
        self.qihu=QtGui.QRadioButton(Form)
        self.qihu.setObjectName(_fromUtf8("qihu"))
        self.sousou=QtGui.QRadioButton(Form)
        self.sousou.setObjectName(_fromUtf8("sousou"))
        self.shenma=QtGui.QRadioButton(Form)
        self.shenma.setObjectName(_fromUtf8("shenma"))
        self.l_se=QtGui.QLabel(Form)
        self.l_se.setObjectName(_fromUtf8("label_0"))
        self.gridLayout.addWidget(self.l_se,0,0,1,1)
        self.gridLayout.addWidget(self.baidu, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.qihu, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.sousou, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.shenma, 0, 4, 1, 1)
        self.textEdit_2 = QtGui.QTextEdit(Form)
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.gridLayout.addWidget(self.textEdit_2, 2, 2, 1, 2)
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 2, 0, 1, 2)
        self.tableView = QtGui.QTableWidget(Form)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.setColumnCount(3)
        self.tableView.setColumnWidth(0,150)
        self.tableView.setHorizontalHeaderLabels([u"关键词",u"网址",u"结果"])
        self.gridLayout.addWidget(self.tableView, 2, 4, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 4, 1, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 2, 1, 2)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 2)
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 3, 2, 1, 2)
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 3, 4, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "排名查询", None))
        self.label_3.setText(_translate("Form", "结果", None))
        self.label.setText(_translate("Form", "网址", None))
        self.label_2.setText(_translate("Form", "关键词", None))
        self.pushButton.setText(_translate("Form", "开始查询", None))
        self.l_se.setText(_translate("Form", "搜索引擎：", None))
        self.baidu.setText(_translate("Form", "百度", None))
        self.qihu.setText(_translate("Form", "360", None))
        self.sousou.setText(_translate("Form", "搜搜", None))
        self.shenma.setText(_translate("Form", "神马", None))
        self.pushButton_2.setText(_translate("Form", "清楚数据", None))
        self.pushButton_3.setText(_translate("Form", "保存", None))

class MainGui(QtGui.QWidget,Ui_Form):
    def __init__(self,parent=None):
        super(MainGui,self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.baidu.setChecked(True)
        self.connect(self.pushButton,QtCore.SIGNAL("clicked()"),self.query)
        self.connect(self.pushButton_3,QtCore.SIGNAL("clicked()"),self.saveData)
        self.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),self.cls)
        self.se="baidu"
    def query(self):
        keys=str(self.textEdit.toPlainText()).split("\n") #分行转换数列
        urls=str(self.textEdit_2.toPlainText()).split("\n")
        urls=[u[:-1].replace("http://","").replace("www.","") if u.strip()[-1:]=="/" else u.replace("http://"," ").replace("www.","") for u in urls] #处理用户输入字符串
        keys=[k.strip() for k in keys] #去除多余空格
        while "" in keys:
            keys.remove("")
        while "" in urls:
            urls.remove("")
        for t in ["baidu","qihu","sousou","shenma"]:
            if getattr(self,t).isChecked():
                self.se=t
        self.q_thread=Query(keys,urls,self)
        self.q_thread.start()
    def cls(self):
        """清除数据"""
        self.textEdit.setText("")
        self.textEdit_2.setText("")
        self.tableView.setRowCount(0)
        if hasattr(self,"q_thread"):
            del self.q_thread 
                   
        QtGui.QMessageBox.information(self,u"提示",u"清楚数据成功！")
        
    def saveData(self):
        u=[] #存放URL的数列
        k=[] #关键词
        r=[] #结果
        
        if hasattr(self,"q_thread"):
            if self.q_thread.is_alive():
                QtGui.QMessageBox.warning(self,u"错误",u"还在查询中请稍后再保存！")
            else:
                for url,pn,index,key in self.q_thread.result:
                    u.append(url)
                    k.append(key)
                    r.append(u"第{}页第{}个".format(pn,index))
                timetag=datetime.datetime.now().strftime('%b%d%y%H%M%S') #生成“时间”文件名
                generate_xls(u,k,r,self.se+timetag)   #调用函数保存xls文件
                QtGui.QMessageBox.information(self,u"提示",u"保存成功！")
                if self.q_thread.result: #清除数据
                    self.q_thread.result=[]
        else:
            QtGui.QMessageBox.critical(self,u"警告",u"请先查询再保存数据！")

    def msg(self,count):
        QtGui.QMessageBox.information(self,u"提示",u"一共{}条结果，查询完毕".format(count))

app=QtGui.QApplication(sys.argv)
win=MainGui()
win.show()
app.exec_()
