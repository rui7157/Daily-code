# coding:utf-8
import wx
import os
import glob
from CodeStatistics import Statistics, isdir

class OnDropFile(wx.FileDropTarget):
    def __init__(self, widgt):
        wx.FileDropTarget.__init__(self)
        self.widgt = widgt

    def OnDropFiles(self, x, y, fileNames):
        self.widgt.SetLabelText(u"正在统计请稍等……")
        allFile = list()
        allFile = isdir(fileNames, allFile)
        result = Statistics(allFile)
        result.count()
        self.widgt.SetLabelText(u"""
一共统计{f}个Python文件
代码行：{c}
注释行：{n}
空白行：{v}
        """.format(f=result.file_num, c=result.c_lines, n=result.n_lines, v=result.v_lines))


class Frame(wx.Frame):
    def __init__(self):
        frame = wx.Frame.__init__(self, None, -1, u"代码统计", pos=(200, 300), size=(300, 150), style=wx.MINIMIZE_BOX |
                                  wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.labelResult = wx.StaticText(
            self.panel, -1, u"拖放文件/文件夹到此处", size=(300, 150),style=wx.ALIGN_CENTER)
        sizer.Add(self.labelResult, wx.EXPAND)
        self.panel.SetSizer(sizer)
        self.labelResult.SetDropTarget(OnDropFile(self.labelResult))

app = wx.App()
Frame().Show()
app.MainLoop()
