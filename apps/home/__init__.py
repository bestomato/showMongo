 #-*- coding:utf-8 -*-

import app

prefix = '/'

urls = [
    # comments
    ('', app.HomeHandler),
    ('/', app.HomeHandler),
]
