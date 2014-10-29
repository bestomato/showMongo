#-*- coding:utf-8 -*-

from base import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):

        #列出server_info信息
        info = self._data_base_conn.server_info()

        #列出全部数据库
        data = self._data_base_conn.database_names()

        self.render('index.html', data=sorted(data))

