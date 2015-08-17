 #-*- coding:utf-8 -*-

import app

prefix = '/dbs'

urls = [
    # comments
    ('', app.HomeHandler),
    ('/left', app.HomeLeftHandler),
    ('/dbs', app.DbListHandler),



    ('/add', app.AddDbsHandler),

]
