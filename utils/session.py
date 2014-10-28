"""
1. define class Session, define the interface to access session data.
   need send session_store and request params.
   session_store should support the set_session() and get_session() method.
   using request object to store the sessionid in to secure cookie.
2. define the RedisSessionStore to store session data into redis server.
   this class provider 3 api: 
   get_session(sid)
   set_session(sid, session_data, expire)
   delete_session(sid)

"""

import cPickle as pickle
from uuid import uuid4
import time
 
class Session(object):

    def __init__(self, session_store, session_transmission, key_prefix='picasso'):
        self._store = session_store
        self.key_prefix = key_prefix

        self._sessionid = session_transmission.get_session_id()
        if not self._sessionid:
            self._sessionid = self._generate_sid()
            session_transmission.set_session_id(self._sessionid)
        
        self._sessiondata = self._store.get_session(self._sessionid)
        self.dirty = False
 
    @property
    def sessionid(self):
        return self._sessionid
 
    def __getitem__(self, key):
        return self._sessiondata.get(key, None)
 
    def __setitem__(self, key, value):
        self._sessiondata[key] = value
        self._dirty()
 
    def __delitem__(self, key):
        del self._sessiondata[key]
        self._dirty()
 
    def __len__(self):
        return len(self._sessiondata)
 
    def __contains__(self, key):
        return key in self._sessiondata
 
    def __iter__(self):
        for key in self._sessiondata:
            yield key
 
    def __repr__(self):
        return self._sessiondata.__repr__()
 
    def __del__(self):
        if self.dirty:
            self._save()
    
    def clear(self):
        self._store.delete_session(self._sessionid)
  
    def _generate_sid(self):
        sid = '%s:%s' % (self.key_prefix, uuid4().get_hex()) 
        if self._store.session_id_exists(sid): 
            sid = self._generate_sid()
        return sid

    def _dirty(self):
        self.dirty = True
 
    def _save(self):
        self._store.set_session(self._sessionid, self._sessiondata)
        self.dirty = False

class CookieSessionIdTransmission(object):

    def __init__(self, handler, cookie_name='__sid'):
        self.handler = handler
        self.cookie_name = cookie_name

    def get_session_id(self):

        return self.handler.get_secure_cookie(self.cookie_name)

    def set_session_id(self, sid):

        self.handler.set_secure_cookie(self.cookie_name, sid)

class UrlSessionIdTransmission(object):

    def __init__(self, handler, key='__sid'):
        self.handler = handler
        self.key = key

    def get_session_id(self):
        return self.handler.get_argument(self.key, None)

    # do nothing, need to add this value into url yourself.
    def set_session_id(self, sid):
        pass

class HeaderSessionIdTransmission(object):

    def __init__(self, handler, header_name='X-Transmission-Session-Id'):
        self.handler = handler
        self.header_name = header_name

    def get_session_id(self):
        return self.handler.request.headers.get(self.header_name)

    def set_session_id(self, sid):
        self.handler.set_header(self.header_name, sid)

class RedisSessionStore(object):
 
    def __init__(self, redis_connection, **options):
        self.options = {
            'field': 'data'
        }
        self.options.update(options)
        self.redis = redis_connection
 
    def get_session(self, sid):
        data = self.redis.hget(sid, self.options['field'])

        return pickle.loads(data) if data else dict()
 
    def set_session(self, sid, session_data, expire = 7200):
        self.redis.hset(sid, self.options['field'], pickle.dumps(session_data))
        self.redis.expire(sid, expire)
 
    def delete_session(self, sid):
        self.redis.delete(sid)

    def session_id_exists(self, sid):
        return sid and self.redis.exists(sid)


if __name__ == '__main__':
    import tornado.ioloop
    import tornado.web
    import redis

    class MainHandler(tornado.web.RequestHandler):

        def get(self, name):

            oname = self.get_current_user() or 'world'
            self.write("Hello, %s, the old name is %s." % (name, oname))
            if oname != name:
                self.session['user'] = name
                self.write("<br />Name not equal set new name %s." % name)

        def get_current_user(self):

            return self.session['user'] if self.session and 'user' in self.session else None

        @property
        def session(self):

            return Session(self.application.settings['session_store'], HeaderSessionIdTransmission(self))

    # TODO session_store
    application = tornado.web.Application([(r"/(.*)", MainHandler)]
        , session_store=RedisSessionStore(redis.Redis())
        , cookie_secret='aVD321fQAGaYdkLlsd334K#/adf22iNvdfdflle3fl$=')

    if __name__ == "__main__":

        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
