#-*- coding:utf-8 -*-

from base import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):

        self.get_ac_conn()


        row = self._coll.find()

        for i in self._coll.find():
            print i



        self.render('index.html')


