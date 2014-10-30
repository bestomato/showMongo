#-*- coding:utf-8 -*-

from base import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        self.render('index.html')



class HomeLeftHandler(BaseHandler):

    def get(self):
        self.render('../public/left.html')


class DbListHandler(BaseHandler):

    def get(self):
        data = self.get_server_database()
        self.render('dbs.html', data=sorted(data))


















