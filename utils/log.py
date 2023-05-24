# -*- coding: utf-8 -*-
# @Time    : ${2021/7/14}
# @File    : Log.py
# !/usr/bin/env python
import logging
import os.path
import time


class Logger(object):
    def __init__(self, logger):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        :param logger:
        """
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        # rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # log_path = os.path.dirname(os.path.abspath('.')) + '\\Log\\Logs\\'
        # log_name = log_path + rq + '.log'
        # error_log_path = os.path.dirname(
        #     os.path.abspath('.')) + '\\Log\\error_logs\\'
        # error_log_name = error_log_path + rq + '.log'
        # fh = logging.FileHandler(log_name, encoding='utf-8')
        # fh.setLevel(logging.INFO)
        # eh = logging.FileHandler(error_log_name, encoding='utf-8')
        # eh.setLevel(logging.ERROR)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # 定义handler的输出格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s  - %(lineno)s - %(message)s')
        # fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # eh.setFormatter(error_formatter)
        # 给logger添加handler
        # self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        # self.logger.addHandler(eh)

    def getlog(self):
        return self.logger


if __name__ == '__main__':
    pass
