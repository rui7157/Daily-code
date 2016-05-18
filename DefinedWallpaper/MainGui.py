#!coding:utf-8
from PyQt4 import QtCore, QtGui
import sys
import os
from setWarpaper import NoteWallpaper

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
from functools import partial


class ArgsError(Exception):
    pass


class Ui_MainWindows(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle(u"笔记壁纸")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(_fromUtf8("ttt.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.filetext = QtGui.QLineEdit(
            os.path.join(os.path.dirname(__file__), ""))
        inputfile = QtGui.QPushButton(u"选择文件")
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(u"壁纸路径:"))
        hbox.addWidget(self.filetext)
        hbox.addWidget(inputfile)

        self.text = QtGui.QTextEdit("")
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(self.text)

        okbutton = QtGui.QPushButton(u"设置")
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addStretch()
        hbox3.addWidget(okbutton)
        hbox3.addStretch()

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        self.setLayout(vbox)

        self.connect(
            inputfile, QtCore.SIGNAL("clicked()"), self.openfile_clicked)
        self.connect(okbutton, QtCore.SIGNAL("clicked()"), self.setup)
        self.resize(600, 400)

    def openfile_clicked(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(
            self, 'Open file', os.path.dirname(__file__), u"图像文件 (*.bmp);;All Files (*)")
        self.filetext.setText(self.filename)

    def nofile(self):
        QtGui.QMessageBox.critical(self, u"警告", u"未选择文件!")

    def errorpath(self):
        QtGui.QMessageBox.critical(self, u"警告", u"错误的文件或路径!")

    def setup(self):
        text = self.text.toPlainText().toLocal8Bit()
        imagepath = self.filetext.text()
        if NoteWallpaper(text=unicode(text, "gbk", "ignore"), imgpath=str(imagepath)).setWallpaper() == "FilePathError":
            self.errorpath()
        else:
            QtGui.QMessageBox.information(self, u"提示", u"设置成功！")

app = QtGui.QApplication(sys.argv)
w = Ui_MainWindows()
# w.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
w.setWindowFlags(
    w.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)  # 禁用最大化按钮
w.show()
app.exec_()
