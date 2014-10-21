 #-*- coding:utf-8 -*-

import app

prefix = '/user'

urls = [
    # comments
    ('/up', app.UserHandler),
]
