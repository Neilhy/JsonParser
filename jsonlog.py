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
        self.file_name = os.path.join(
            'e:/JsonParser', "log", local_time+'.log'
        )  # 日志保存在log目录下
        # self.filename = self.path + os.path.sep + local_time + '.log'  # 日志文件名称
        self.name = name
        self.formatter = logging.Formatter(
            # '%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s - %(message)s'
            '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        )
        self.file_handler = logging.handlers.TimedRotatingFileHandler(
            self.file_name, 'D', 1, 10)  # 日志保留10天，一天保存一个文件
        # self.file_handler = logging.handlers.RotatingFileHandler(
        #     self.filename, maxBytes=1024 * 1024, backupCount=5
        # )
        self.file_handler.setFormatter(self.formatter)
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)  # 控制日志文件中记录级别
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.INFO)
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

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, args, kwargs)
