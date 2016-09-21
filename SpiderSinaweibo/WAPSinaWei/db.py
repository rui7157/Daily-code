#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-19 15:19:20
# @Author  : NvRay (nvray@foxmail.com)


from pymongo import MongoClient


class DbConn(object):

    def __init__(self,host="127.0.0.1",port=27017):
        self.server="mongodb://{host}:{port}".format(host=host,port=port)
        self.conn=None
    def connect(self):    
        self.conn=MongoClient(self.server)
    def close(self):
        return self.conn.disconnect()
    def getConn(self):
        return self.conn

dbconn=DbConn()

def process():
    #建立连接
    dbconn.connect()
    global conn
    conn = dbconn.getConn()

    #列出server_info信息
    print conn.server_info()

    #列出全部数据库
    databases = conn.database_names()
    print databases

    #删除库和表
    dropTable()
    #添加数据库lifeba及表(collections)users
    createTable()
    #插入数据
    insertDatas()
    #更新数据
    updateData()
    #查询数据
    queryData()
    #删除数据
    deleteData()

    #释放连接
    dbconn.close()

def insertDatas():
    datas=[{"name":"steven1","realname":"测试1","age":25},
           {"name":"steven2","realname":"测试2","age":26},
           {"name":"steven1","realname":"测试3","age":23}]
    lifeba_users.insert(datas)

def updateData():
    '''只修改最后一条匹配到的数据
           第3个参数设置为True,没找到该数据就添加一条
           第4个参数设置为True,有多条记录就不更新
    '''
    lifeba_users.update({'name':'steven1'},{'$set':{'realname':'测试1修改'}}, False,False)

def deleteData():
    lifeba_users.remove({'name':'steven1'})

def queryData():
    #查询全部数据
    rows = lifeba_users.find()
    printResult(rows)
    #查询一个数据
    print lifeba_users.find_one()
    #带条件查询
    printResult(lifeba_users.find({'name':'steven2'}))
    printResult(lifeba_users.find({'name':{'$gt':25}}))

def createTable():
    '''创建库和表'''
    global lifeba_users
    lifeba_users = conn.lifeba.users

def dropTable():
    '''删除表'''
    global conn
    conn.drop_database("lifeba")

def printResult(rows):
    for row in rows:
        for key in row.keys():#遍历字典
            print row[key], #加, 不换行打印
        print ''