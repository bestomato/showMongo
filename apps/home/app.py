#-*- coding:utf-8 -*-

from base import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        #列出全部数据库
        data = self.get_server_database()

        self.render('index.html', data=sorted(data))











class guodong(BaseHandler):

    def get(self):


        print 123



class guodong1(BaseHandler):

    def get(self):

        self.render('kkk.html')



class guodong2(BaseHandler):

    def get(self):


        self.render('kkk1.html', bianliang='woshibairui')


