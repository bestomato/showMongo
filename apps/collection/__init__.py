 #-*- coding:utf-8 -*-

import app

prefix = '/coll'

urls = [
    # comments
    ('', app.HomeHandler),
    ('/delete', app.CollDeleteHandler),

]
