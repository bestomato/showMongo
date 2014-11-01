#-*- coding:utf-8 -*-

from base import BaseHandler
from setting import (TEMPLATE_PATH as _TEMPLATE_PATH)

class HomeHandler(BaseHandler):

    _get_params = {
            'option':[
                ('db', basestring, ''),
                ('coll', basestring, ''),
                ('page', int, 1),
            ]
        }


    def get(self):

        collArr = self._coll.find()

        for i in collArr:
            print i


        paramList = {
            'db': self._params['db'],
            'coll': self._params['coll']
        }
        pageHtml = self.get_page_info(self._page, paramList)

        self.render('index.html', pageHtml=pageHtml, d=[1,2,3,4,5,6,7,8])


