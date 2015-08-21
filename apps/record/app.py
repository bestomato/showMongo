#-*- coding:utf-8 -*-

import types
import json
from bson.objectid import ObjectId
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
                value_str.strip()
                json_str = json.loads(value_str)

                if json_str != {}:
                    query = json_str
                else:
                    query = dict()

                # query = eval(json_str)
                # print query
                # if types(query) == types(dict()):
                #     pass

                # query = dict()
                #
                # value_str.strip()
                # value_str[1:-1]
                # value_str_list = value_str.split(',')
                # for i in value_str_list:
                #     i.strip()
                #     value_str_list_i = i.split(':')
                #
                #     query[]


            except Exception as e:
                query_status = 'error'
                query = dict()
        else:
            value_str = None
            query = dict()


        collArr = self._coll.find(query).limit(self.page_num_data).skip(skip).sort('_id',-1)
        count = self._coll.find(query).count() - skip

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
                    d=result)


class RecordAddHandler(BaseHandler):

    _post_params = {
            'option':[
                ('query', basestring, ''),
                ('db', basestring, ''),
                ('coll', basestring, ''),
            ]
        }

    _get_params = {
            'option':[
                ('query_status', basestring, ''),
                ('query', basestring, ''),
                ('db', basestring, ''),
                ('coll', basestring, ''),
            ]
        }


    def get(self):
        self.render('add.html',
                    query='',
                    query_status='')

    def post(self):
        query_str = ''
        query_status = ''

        query = None
        value_str = self._params['query']
        try:
            value_str.strip()
            json_str = json.loads(value_str)

            if json_str != {}:
                query = json_str

        except Exception as e:
            print e
            query_status = 'error'

        if query:
            if self._coll.insert(query):
                self.redirect('/record?db=%s&coll=%s' % (self._dbs_value, self._coll_value))

        else:
            query_status = 'error'

        self.render('add.html',
                    query=query_str,
                    query_status=query_status)


class RecordDeleteHandler(BaseHandler):

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


class RecordRestHandler(BaseHandler):

    _post_params = {
            'option':[
                ('query', basestring, ''),
                ('db', basestring, ''),
                ('coll', basestring, ''),
                ('id', basestring, ''),
            ]
        }

    _get_params = {
            'option':[
                ('query_status', basestring, ''),
                ('query', basestring, ''),
                ('db', basestring, ''),
                ('coll', basestring, ''),
                ('id', basestring, ''),
            ]
        }


    def get(self):
        data = self._coll.find_one({"_id":ObjectId(self._params['id'])})
        # for i in data:
        #     if isinstance(data[i], ObjectId):
        #         data[i] = str(data[i])
        #
        # data = json.dumps(data, ensure_ascii=False)

        self.render('up.html',
                    query=sorted(data),
                    query_status='')

    def post(self):
        query_str = ''
        query_status = ''

        query = None
        value_str = self._params['query']
        try:
            value_str.strip()
            json_str = json.loads(value_str)

            if json_str != {}:
                query = json_str

        except Exception as e:
            print e
            query_status = 'error'

        if query:
            if self._coll.insert(query):
                self.redirect('/record?db=%s&coll=%s' % (self._dbs_value, self._coll_value))

        else:
            query_status = 'error'

        self.render('up.html',
                    query=query_str,
                    query_status=query_status)



