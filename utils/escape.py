# -*- coding:utf-8 -*-

from datetime import datetime
import time
import json
import base64
import hashlib
import logging

from urllib import unquote
from bson.objectid import ObjectId

logger = logging.getLogger('root.util.escape')

def to_list_str(value):
    """递归序列化list
    """
    for index, v in enumerate(value):
        if isinstance(v, dict):
            value[index] = to_dict_str(v)
            continue

        if isinstance(v, list):
            value[index] = to_list_str(v)
            continue

        value[index] = default_encode(v)

    return value


def to_dict_str(value):
    """递归序列化dict
    """
    for k, v in value.items():
        if isinstance(v, dict):
            value[k] = to_dict_str(v)
            continue

        if isinstance(v, list):
            value[k] = to_list_str(v)
            continue

        value[k] = default_encode(v)

    return value


def default_encode(v):
    """数据类型转换
    """
    if isinstance(v, ObjectId):
        return str(v)

    if isinstance(v, datetime):
        return format_time(v)

    return v

def format_dt(dt, ft='%Y-%m-%d %H:%M'):
    return dt.strftime(ft)

def format_time(t, ft='%Y-%m-%d %H:%M', micro=True):
    return time2datetime(t, micro).strftime(ft)

def recursive_to_str(v):
    if isinstance(v, list):
        return to_list_str(v)

    if isinstance(v, dict):
        return to_dict_str(v)

    return default_encode(v)


def to_objectid(objid):
    """字符对象转换成objectid
    """  
    if objid is None:
        return objid
        
    try:
        objid = ObjectId(objid)
    except:
        logger.error("%s is invalid objectid" % objid)
        return None
    
    return objid


def json_encode(data):
    try:
        return json.dumps(data)
    except Exception as e:
        logger.error(e)


def json_decode(data):
    try:
        return json.loads(data)
    except Exception as e:
        logger.error(e)

def to_int(value, default=None):
    try:
        return int(value)
    except ValueError as e:
        logger.error(e)

def to_float(value, default=None):
    try:
        return float(value)
    except ValueError as e:
        logger.error(e)



#datetime to time
def time2datetime(t, micro=True):
    if micro:
        return datetime.fromtimestamp(t/1000)
    else:
        return datetime.fromtimestamp(t)

#time to datetime
def datetime2time(t, micro=True):
    if micro:
        return long(time.mktime(t.timetuple())*1000)
    else:
        return long(time.mktime(t.timetuple()))


def get_now_utc_time():

    # 获取utc时间,如果有直接获取utc时间戳的那么能优化
    utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # 获取当前系统时区的时间
    local = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")

    # 将utc时间转化为时间戳
    timeArray1 = time.strptime(utc, "%Y-%m-%d %H:%M:%S")
    timeStamp1 = int(time.mktime(timeArray1))

    # 将本服务器时区时间转化为时间戳
    timeArray2 = time.strptime(local, "%Y-%m-%d %H:%M:%S")
    timeStamp2 = int(time.mktime(timeArray2))

    # 获取他们的时间差,用来更正入库时间戳
    return timeStamp1 - timeStamp2
