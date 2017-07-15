#! /usr/bin/env python
# -*- coding:utf -*-

import logging
import logging.handlers
import time
import sys
import os.path

local_time = time.strftime('%Y%m%d', time.localtime(time.time()))


class JsonLog(object):
    """JsonParser's log"""

    def __init__(self, name):
        self.path = os.path.join(sys.path[0], "log")  # 日志保存在log目录下
        self.filename = self.path + local_time + '.log'  # 日志文件名称
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)  # 控制日志文件中记录级别
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.INFO)
        self.file_handler = logging.handlers.TimedRotatingFileHandler(
            self.filename, 'D', 1, 10)  # 日志保留10天，一天保存一个文件
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, args, kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, args, kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, args, kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, args, kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, args, kwargs)

    def fatal(self, msg, *args, **kwargs):
        self.logger.fatal(msg, args, kwargs)
