#-*- coding:utf-8 -*-

from pymongo import DESCENDING, ASCENDING

import time
import loggers
from datetime import datetime
from models.monitor import model as monitor_db
from models.user import model as user_db


from base import BaseHandler

class UserHandler(BaseHandler):

    _get_params = {
            'option':[
                ('info', int, 0),
            ]
        }


    def get(self):

        # 说明是要拉取新的数据
        if self._params['info']:
            self._getNewData()


        result = list(monitor_db.User().find({}, limit=15, sort=[('ontime', DESCENDING)]))
        # {u'_id': ObjectId('543653ace49247bd038b4567'), u'number': 2004.0, u'ontime': 1412784000.0}
        data = []
        data_info = []
        for i in result:
            ontime = str(i['ontime'] / 1000)

            t = datetime.fromtimestamp(int(ontime)).strftime("%Y-%m-%d")
            number = int(i['number'])
            data.append([t, number])

            txt = "%s(%s)" % (t,number)
            data_info.append([t, txt])

        self.render('user.html', arr=data, arrtwo=data_info)


    def _getNewData(self):

        oneDayTime = 48 * 3600 * 1000
        tadayTime = int(time.time()) * 1000

        # 查看统计表最新时间,如果和现在差距在48小时之内,说明是最新统计无需拉去
        result = list(monitor_db.User().find({}, limit=1, sort=[('ontime', DESCENDING)]))

        if result:
            partTime = int(result[0]['ontime'])
            if tadayTime - partTime < oneDayTime:
                return
        else:
            # 没有进行过同步首次读取数据
            info = list(user_db.UserAccount().find({}, limit=1, sort=[('atime', ASCENDING)]))

            if info:
                tday = datetime.fromtimestamp(int(info[0]['atime']/1000)).strftime("%Y-%m-%d")
                timeArray = time.strptime(tday, "%Y-%m-%d")
                partTime = int(time.mktime(timeArray)) * 1000 - oneDayTime / 2

                if tadayTime - partTime < oneDayTime:
                    return
            else:
                # 没有用户,直接退出
                return

        # 按照拉去时间差,取组织时间查询条件查询用户增加数据
        newTime = partTime

        while tadayTime - newTime > oneDayTime:
            partTime = newTime
            newTime = newTime + oneDayTime / 2

            # 查询增加一天后的数据
            count = user_db.UserAccount().find({"atime":{"$gte":partTime,"$lt":newTime}}).count()

            # 数据入库
            monitor_db.User().create({"ontime":newTime, "number":int(count)})