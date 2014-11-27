 #-*- coding:utf-8 -*-

import app

prefix = '/'

urls = [
    # comments
    ('', app.HomeHandler),
    ('home/left', app.HomeLeftHandler),
    ('home/dbs', app.DbListHandler),


]
