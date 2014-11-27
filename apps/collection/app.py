#-*- coding:utf-8 -*-

import types
import json

from base import BaseHandler
from setting import (TEMPLATE_PATH as _TEMPLATE_PATH)

class HomeHandler(BaseHandler):

    page_num_data = 10

    _get_params = {
            'option':[
                ('query', basestring, ''),
                ('db', basestring, ''),
                ('coll', basestring, ''),
                ('page', int, 1),
            ]
        }


    def get(self):

        page = self._params['page']
        skip = 0
        if page > 1:
            skip = (page - 1) * self.page_num_data


        query_status = 'success'
        if self._params['query']:
            value_str = self._params['query']
            try:
                # json_str = json.loads(value_str)
                query = eval(value_str)
                # print query
                # if types(query) == types(dict()):
                #     pass


            except Exception as e:
                query_status = 'error'
                query = dict()
        else:
            value_str = None
            query = dict()


        collArr = self._coll.find().limit(self.page_num_data).skip(skip).sort('_id',-1)
        count = self._coll.find().count() - skip

        result = []
        for i in collArr:
            now = {}
            now['str'] = str(i)

            row = {}
            for d in i:
                nt = type(i[d])
                row[d] = "%s-%s" % (str(nt), i[d])

            now['arr'] = i
            now['s'] = count

            count -= 1

            result.append(now)


        paramList = {
            'db': self._params['db'],
            'coll': self._params['coll']
        }
        pageHtml = self.get_page_info(self._page, paramList)

        self.render('index.html',
                    pageHtml=pageHtml,
                    query=value_str,
                    query_status=query_status,
                    d=result, hh='\r\n\r\n\r\n\r\n')


class CollDeleteHandler(BaseHandler):

    _get_params = {
            'option':[
                ('db', basestring, ''),
                ('coll', basestring, ''),
                ('id', basestring, ''),
            ]
        }


    def get(self):

        if self._params['id']:
            id = self.to_objectid(self._params['id'])
            end = self._coll.remove({"_id":id})
            if end:
                self.write({"data":"yes"})
            else:
                self.write({"data":"no"})






