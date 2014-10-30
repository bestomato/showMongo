#-*- coding:utf-8 -*-

from base import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        #列出全部数据库
        data = self.get_server_database()

        self.render('index.html', data=sorted(data))

