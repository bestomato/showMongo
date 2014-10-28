#-*- coding:utf-8 -*-

import os
import sys
import logging

import setting

def _getSimpleHanlder(logfile, maxBytes=500*1024*1024, backupCount=3):
    #root logger default warning change to debug
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    simple_formater = logging.Formatter('%(levelname)s:%(asctime)s %(name)s:%(lineno)d:%(funcName)s %(message)s')

    from logging import handlers
    fh = handlers.RotatingFileHandler(logfile, maxBytes=maxBytes, backupCount=backupCount)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(simple_formater)
    ch.setFormatter(simple_formater)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def getLogger(currfile, logfile=None, maxBytes=500*1024*1024, backupCount=3):
    if logfile:
        return _getSimpleHanlder(logfile, maxBytes, backupCount)

    path = os.path.abspath(currfile)
    if not os.path.isfile(path):
        raise Exception("%s is invalid module" % currfile)

    file_name = os.path.basename(path)
    dot_index = file_name.rfind('.')
    if dot_index < 0:
        raise Exception("%s is invliad python file" % currfile)
    
    module_name = file_name[0:dot_index]
    logger_name_list = [module_name]
    
    # find server root dir util find it or to root dir '/'
    while 1:
        path = os.path.dirname(path)     
        dirname = os.path.basename(path)
        if dirname == setting.SERVER_NAME or dirname == '/':
            break
        logger_name_list.append(dirname)

    logger_name_list.reverse()

    logger = logging.getLogger('.'.join(logger_name_list))
    if not logger.handlers:
        return logging.getLogger('.'.join([logging.root.name, logger.name]))
    else:
        return logger
