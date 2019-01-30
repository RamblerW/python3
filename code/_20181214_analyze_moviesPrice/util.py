#!/usr/bin/env python
#-*- coding:utf-8 -*-

# author: rambler
# datetime: 2018/12/14 21:02
# software: PyCharm

# 获取数据库连接
import datetime
import traceback

import pymongo

# 获取数据库
def getDB():
    conn = pymongo.MongoClient('mongodb://localhost:27017/')
    db = conn.moviePrice  # 表名
    return conn, db

# 保存数据到mongoDB
def saveData(list,collectionName):
    conn, db = getDB()
    try:
        # 保存数据
        db[collectionName].insert_many(list)
        print(datetime.datetime.now(), collectionName, 'saveData success', len(list))
    except Exception as e:
        print("saveData Error")
        traceback.print_exc()
    finally:
        conn.close()