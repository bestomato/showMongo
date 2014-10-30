 #-*- coding:utf-8 -*-

import app

prefix = '/'

urls = [
    # comments
    ('', app.HomeHandler),
    ('/', app.HomeHandler),
    ('guodong', app.guodong),
    ('guodong1', app.guodong1),
    ('guodong2', app.guodong2),
]
