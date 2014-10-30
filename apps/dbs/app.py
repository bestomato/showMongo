#-*- coding:utf-8 -*-

from base import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        print 1


        self.render('index.html')


