#-*- coding:utf-8 -*-

import logging
import re

from datetime import  datetime

import tornado.web
import tornado.escape

from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId

from settings import CDN as _CDN
import loggers

logger = loggers.getLogger(__file__)

from utils import (escape as _es, httputil as _ht)


class BaseBaseHandler(tornado.web.RequestHandler):


    _types = [ObjectId, None, basestring, int, float, list, file]


    def initialize(self):
        # request context
        self.context = self.get_context()

        # app template path if exist must end with slash like user/
        self.template_path = ''


    def render(self, template_name, **kwargs):
        super(BaseBaseHandler, self).render(('%s%s') % (self.template_path, template_name),
            context=self.context,
            nowurl=self.request.path,
            **kwargs)

    def sort_by(self, sort):
        return {1: ASCENDING, -1: DESCENDING}.get(sort, ASCENDING)

    # request context
    def get_context(self):
        return {


        }

    def static_url(self,  path, include_host=None, v=None, **kwargs):
        is_debug = self.application.settings.get('debug', False)

        # In debug mode, load static files from localhost
        if is_debug or not _CDN['is']:
            return super(BaseBaseHandler, self).static_url(path, include_host, **kwargs)

        v = kwargs.get('v','')

        if v:
            return ('%s/%s?v=%s')%(_CDN['host'], path, v)
        else:
            return ('%s/%s')%(_CDN['host'], path)

    def to_objectid(self, objid):
        return _es.to_objectid(objid)

    def to_int(self, value):
        return _es.to_int(value)

    def to_float(self, value):
        return _es.to_float(value)
    
    def utf8(self, v):
        return tornado.escape.utf8(v)

    def encode_http_params(self, **kw):
        '''
        url parameter encode
        '''
        return _ht.encode_http_params(**kw) 

    def json_encode(self, data):
        return _es.json_encode(data)

    def json_decode(self, data):
        return _es.json_decode(data)
        
    def recur_to_str(self,v):
        return _es.recursive_to_str(v)

    def prepare(self):
        pass



    @property
    def parameter(self):
        '''
        according to request method config to filter all request paremter
        if value is invalid then set None
        '''
        method = self.request.method.lower()
        arguments = self.request.arguments
        files = self.request.files

        params = getattr(self, '_%s_params' % method, None)
        if params is None:
            return {}

        rpd = {} # request parameter dict
        def filter_parameter(key, tp, default=None):
            if tp not in self._types:
                raise ValueError("%s parameter expected types %s" % (key, self._types))
            
            if tp != file:
                if key not in arguments:
                    rpd[key] = default 
                    return  

                if tp in [ObjectId, int, float]:
                    rpd[key] = getattr(self, 'to_%s'%getattr(tp, '__name__').lower())(self.get_argument(key))
                    return  

                if tp == basestring:
                    rpd[key] = self.get_argument(key, strip=True)
                    return 

                if tp == list:
                    rpd[key] = self.get_arguments(key)
                    return 

            if tp == file:
                if key not in files:
                    rpd[key] = default 
                    return 

                rpd[key] = self.request.files[key]

        for key, tp in params.get('need', []):
            if tp == list:
                filter_parameter(key, tp, [])
            else:
                filter_parameter(key, tp)

        for key, tp, default in params.get('option', []):
            filter_parameter(key, tp, default)

        return rpd

    def datetime2time(self, t, ft='%Y-%m-%d'):
        if isinstance(t, basestring):
            return _es.datetime2time(datetime.strptime(t, ft))
        return _es.datetime2time(t)

    def format_time(self, t, ft='%Y-%m-%d %H:%M'):
        if t:
            return _es.format_time(t, ft)

        return ''

    def format_dt(self, dt, ft='%Y-%m-%d %H:%M'):
        return _es.format_dt(dt, ft)

    def http_error(self, status_code=404, **kwargs):
        raise tornado.web.HTTPError(status_code)


class BaseHandler(BaseBaseHandler):

    IMG_WIDTH = 598
    IMG_HEIGHT = 598

    def initialize(self):
        super(BaseHandler, self).initialize()
        self._params = self.parameter
    
    def get_context(self):
        context = super(BaseHandler, self).get_context()
        context.update({
            'path': self.request.path,
            })

        return context

    # write output json
    def wo_json(self, data):
        callback = self._params.get('jsoncallback')
        if callback:
            return self.write('%s(%s)' % (callback, self.json_encode(self.recur_to_str(data))))

        self.write(self.json_encode(data))
            
    # read in json
    def ri_json(self, data):
        return self.json_decode(data)


    def get_file_prefix(self, filename):
        if isinstance(filename, basestring):
            if filename.endswith('.jpg'):
                return '.jpg'

            if filename.endswith('.png'):
                return '.png'

            if filename.endswith('.gif'):
                return '.gif'

        return ''

    def get_page_info(self, page, paramList={}):
        outStr = '<div class="pure-g" > \
                    <div class="pure-u-1-1" > \
                        <div class="m-paginator" > \
                            <ul class="pure-paginator">'
        outStr2 = '         </ul> \
                        </div> \
                    </div> \
                </div>'

        lastUrl = self.context['path']+'?'
        for i in paramList:
            lastUrl += str(i) + '=' + str(paramList[i]) + '&'

        sign = True
        nowPage = page
        whileNum = 0
        pageNum = []
        while sign:
            if nowPage == 0 or whileNum == 4:
                sign = False
            else:
                pageNum.append(nowPage)
                nowPage -= 1
                whileNum += 1
        for i in range(page+1, 8-len(pageNum)+page):
            pageNum.append(i)

        liStr = '<li><a class="pure-button prev" href="' + lastUrl + 'page=' + str(page-1) + '">&#171;</a></li>'
        pageNum.sort()
        for i in pageNum:
            if i == page:
                liStr += '<li><a class="pure-button pure-button-active " href="javascript:void(0)">' + str(i) + '</a></li>'
            else:
                liStr += '<li><a class="pure-button" href="' + lastUrl + 'page=' + str(i) + '">' + str(i) + '</a></li>'
        liStr += '<li><a class="pure-button next" href="' + lastUrl + 'page=' + str(page+1) + '">&#187;</a></li>'
        liStr = '<li><a class="pure-button" href="' + lastUrl + 'page=1" style="color:#999">第一页</a></li>' + liStr
        html = outStr + liStr + outStr2
        return html


class ListBaseHandler(BaseHandler):

    def initialize(self):
        super(ListBaseHandler, self).initialize()
        self._page = 1
    
    def prepare(self):
        super(ListBaseHandler, self).prepare()
        self._page = abs(self._params['page']) if self._params.get('page', None) else 1
        self._max_code = self.get_argument('max_code', None)
        path = self.request.path
