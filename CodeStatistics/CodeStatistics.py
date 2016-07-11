# coding:utf-8
import os
import sys
import glob
import getopt


print u"""
+----------------------------------------+
|           Author:NvRay                 |
|           Date:2016-6-13               |
| 说明：用于统计Python代码行数           |
| 输入参数 -f <python文件路径或目录>     |
+----------------------------------------+
"""


class Statistics(object):

    def __init__(self, file):
        self.files=file
        self.c_lines = 0  # 代码行数
        self.n_lines = 0  # 注释行数
        self.v_lines = 0  # 空行

    def readfile(self, file):
        print file
        code = open(file)
        while 1:
            linecode = code.readline()
            if linecode:
                linecode = linecode.strip()
                if linecode == "":
                    self.v_lines += 1
                elif linecode[0] == "#":
                    self.n_lines += 1

                else:
                    self.c_lines += 1
            else:
                break

    def count(self):
        self.file_num = 0
        for file in self.files:
            self.file_num += 1
            self.readfile(file)
        print u"一共{num}个文件，处理完毕！".format(num=self.file_num)

def isdir(paths,files):
    hasdir=False
    dirAll=[]
    for f in paths:
        if os.path.isdir(f):
            hasdir=True
            dirAll+=glob.glob(f+os.sep+"*")
        else:
            if f[-3:]==".php":
                files.append(f)
    if not hasdir:
        return files
    return isdir(dirAll,files)




if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "hf:", ["help", "file"])
    for opt, value in opts:
        if opt in ["-h", "--help"]:
            print """
None Options:
Current Python's dir.

General Options:
-h, --help                  Show help.
-f, --file <path/dirpath>   File or dir(String).
            """
            sys.exit()
        elif opt in ["-f", "--file"]:
            if os.path.isdir(value):
                files=[]
                files=isdir([value],files)
            else:
                if not os.path.exists(value):
                    print u"文件不存在"
                    sys.exit()
                else:
                    files = [value]
            result = Statistics(files)
        else:
            result = Statistics([os.path.dirname(__file__)])
        result.count()
        print u"""
#############结果#############
代码
总行数：{c}
注释行：{n}
空白行：{v}
#############################
        """.format(c=result.c_lines, n=result.n_lines, v=result.v_lines)
