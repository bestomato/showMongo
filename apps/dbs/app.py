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



class AddDbsHandler(BaseHandler):

    _post_params = {
            'option':[
                ('name', basestring, ''),
            ]
        }


    def get(self):
        if self._params['id']:
            self.render('index.html')

    def post(self):
        if self._params['id']:
            self.render('index.html')