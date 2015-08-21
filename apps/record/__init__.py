 #-*- coding:utf-8 -*-

import app

prefix = '/record'

urls = [
    # comments
    ('', app.HomeHandler),
    ('/delete', app.RecordDeleteHandler),
    ('/add', app.RecordAddHandler),
    ('/rest', app.RecordRestHandler),
]
