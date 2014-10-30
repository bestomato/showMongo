# -*- coding:utf-8 -*-

import os

from pymongo import MongoReplicaSetClient
from pymongo import MongoClient
import gridfs

import setting

if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '__test__')):
    mc = MongoClient(host='localhost')
    mc.slave_okay = True
else:
    mc = MongoReplicaSetClient(host=','.join(setting.HOSTS), replicaSet=setting.REPL_SET_NAME)




class BaseBaseModel(object):

    conn = None
    database = None
    servers = "mongodb://localhost:27017"

    def __init__(self, db=''):
        self.connect()
        self.selectDB(db)

    def connect(self):
        self.conn = MongoClient(self.servers)

    def close(self):
        return self.conn.disconnect()

    def getConn(self):
        return self.conn

    def selectDB(self, name=''):
        if name:
            self.database = self.conn[name]





class BaseModel(BaseBaseModel):

    def __init__(self, db=''):
        super(BaseModel, self).__init__(db)

    def getSeverInfo(self):
        return self.conn.server_info()

    def getDdataBaseName(self):
        return self.conn.database_names()


    def getDataBase(self, name=''):
        if name:
            self.selectDB(name)

        return self.database


    def getCollectionsName(self, name=''):
        if name:
            return self.conn[name].collection_names()


    def getAccount(self, name=''):
        if name:
            return self.database[name]



#     连接数据库
# >>> db = conn.ChatRoom
# 或
# >>> db = conn['ChatRoom']
#
# 连接聚集
# >>> account = db.Account
# 或
# >>> account = db["Account"]
#
# 查看全部聚集名称
# >>> db.collection_names()
#
# 查看聚集的一条记录
# >>> db.Account.find_one()
# >>> db.Account.find_one({"UserName":"keyword"})
#
# 查看聚集的字段
# >>> db.Account.find_one({},{"UserName":1,"Email":1})
# {u'UserName': u'libing', u'_id': ObjectId('4ded95c3b7780a774a099b7c'), u'Email': u'libing@35.cn'}
# >>> db.Account.find_one({},{"UserName":1,"Email":1,"_id":0})
# {u'UserName': u'libing', u'Email': u'libing@35.cn'}
#
# 查看聚集的多条记录
# >>> for item in db.Account.find():
#         item
# >>> for item in db.Account.find({"UserName":"libing"}):
#         item["UserName"]
#
# 查看聚集的记录统计
# >>> db.Account.find().count()
# >>> db.Account.find({"UserName":"keyword"}).count()
#
# 聚集查询结果排序
# >>> db.Account.find().sort("UserName")  --默认为升序
# >>> db.Account.find().sort("UserName",pymongo.ASCENDING)   --升序
# >>> db.Account.find().sort("UserName",pymongo.DESCENDING)  --降序
#
# 聚集查询结果多列排序
# >>> db.Account.find().sort([("UserName",pymongo.ASCENDING),("Email",pymongo.DESCENDING)])
#
#
# 添加记录
# >>> db.Account.insert({"AccountID":21,"UserName":"libing"})
#
# 修改记录
# >>> db.Account.update({"UserName":"libing"},{"$set":{"Email":"libing@126.com","Password":"123"}})
#
# 删除记录
# >>> db.Account.remove()   -- 全部删除
# >>> db.Test.remove({"UserName":"keyword"})

