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




import pymongo

class DBConn:
    conn = None
    servers = "mongodb://localhost:27017"

    def connect(self):
        self.conn = pymongo.Connection(self.servers)

    def close(self):
        return self.conn.disconnect()

    def getConn(self):
        return self.conn

