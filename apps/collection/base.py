#-*- coding:utf-8 -*-

from apps import base

from setting import (TEMPLATE_PATH as _TEMPLATE_PATH)

class BaseHandler(base.BaseHandler):

    def initialize(self):
        super(BaseHandler,self).initialize()
        self.template_path = _TEMPLATE_PATH

        self._page = 1


    def prepare(self):
        self._page = abs(self._params['page']) if self._params.get('page', None) else 1
